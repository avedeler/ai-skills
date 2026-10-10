#!/usr/bin/env python3
"""Check a development evidence packet for consistency, not truth or authority.

No subprocesses, network, test execution, dispatch, or repository mutation.
Policy and expected candidate must come from the trusted coordinating host.
"""

import argparse
import json
from pathlib import Path
import re
import sys


def text(value):
    return isinstance(value, str) and bool(value.strip())


def check(policy, packet, expected_candidate, allow_synthetic=False):
    """Return gaps without executing or authenticating the supplied evidence.

    Policy is the host-reviewed obligation set. A failed correction count at its
    stop limit blocks further automatic progress; a zero-repair policy still
    permits a candidate that has had no failed correction rounds.
    """
    errors = []
    if not isinstance(policy, dict) or not isinstance(packet, dict):
        return ["Policy and packet must be JSON objects"]
    if not isinstance(expected_candidate, str) or not re.fullmatch(r"sha256:[0-9a-f]{64}", expected_candidate):
        return ["Expected candidate must be a trusted sha256 content identity"]
    for label, value in (("policy", policy), ("packet", packet)):
        if type(value.get("schema_version")) is not int or value["schema_version"] != 1:
            errors.append(f"{label}: unsupported schema_version")
    if type(packet.get("synthetic")) is not bool:
        errors.append("packet: synthetic must be explicitly true or false")
    elif packet["synthetic"] and not allow_synthetic:
        errors.append("Synthetic evidence is not live readiness evidence")
    if packet.get("candidate") != expected_candidate:
        errors.append("Packet candidate differs from expected candidate")

    required = policy.get("required_checks")
    if not isinstance(required, list) or not required or not all(text(item) for item in required):
        errors.append("policy: required_checks must be a nonempty string list")
        required = []
    elif len(required) != len(set(required)):
        errors.append("policy: duplicate required check IDs")
    requirements = policy.get("requirements")
    if not isinstance(requirements, dict):
        errors.append("policy: requirements must map requirement IDs to scenario lists")
        requirements = {}
    expected_pairs = set()
    for requirement, scenarios in requirements.items():
        if not text(requirement) or not isinstance(scenarios, list) or not scenarios or not all(text(s) for s in scenarios):
            errors.append("policy: invalid requirement/scenario mapping")
            continue
        if len(scenarios) != len(set(scenarios)):
            errors.append(f"policy: duplicate scenario for {requirement}")
        expected_pairs.update((requirement, scenario) for scenario in scenarios)
    for flag in ("security_required", "spec_sync_required"):
        if type(policy.get(flag)) is not bool:
            errors.append(f"policy: {flag} must be a boolean")
    limit = policy.get("max_failed_correction_rounds")
    if type(limit) is not int or limit < 0:
        errors.append("policy: correction limit must be a nonnegative integer")
        limit = 0

    authors = packet.get("author_sessions")
    if not isinstance(authors, list) or not authors or not all(text(a) for a in authors):
        errors.append("packet: author_sessions must identify the actual author contexts")
        authors = []

    def receipt(label, value, statuses=("passed",), executed=False, independent=False):
        if not isinstance(value, dict):
            errors.append(f"{label}: missing receipt")
            return
        if value.get("candidate") != expected_candidate:
            errors.append(f"{label}: stale or missing candidate identity")
        if value.get("status") not in statuses:
            errors.append(f"{label}: required result is not {','.join(statuses)}")
        if not text(value.get("evidence")):
            errors.append(f"{label}: missing raw evidence reference")
        if executed and (type(value.get("exit_code")) is not int or value["exit_code"] != 0):
            errors.append(f"{label}: successful command exit evidence is required")
        if independent and (not text(value.get("session_id")) or value["session_id"] in authors):
            errors.append(f"{label}: independent non-author review context is required")

    receipt("planning", packet.get("planning"))
    receipt("tasks", packet.get("tasks"))
    checks = packet.get("checks")
    if not isinstance(checks, dict):
        errors.append("packet: checks must be an object")
        checks = {}
    for name in required:
        receipt(f"check {name}", checks.get(name), executed=True)

    traceability = packet.get("traceability")
    if not isinstance(traceability, list):
        errors.append("packet: traceability must be an array")
        traceability = []
    covered = set()
    for entry in traceability:
        if not isinstance(entry, dict):
            errors.append("traceability: expected an object")
            continue
        requirement, scenario = entry.get("requirement"), entry.get("scenario")
        if not text(requirement) or not text(scenario):
            errors.append("traceability: missing requirement/scenario IDs")
            continue
        pair = (requirement, scenario)
        if pair in covered:
            errors.append(f"traceability: duplicate mapping {pair}")
        covered.add(pair)
        if pair not in expected_pairs:
            errors.append(f"traceability: scenario outside reviewed policy {pair}")
        if entry.get("check") not in required:
            errors.append(f"traceability: {pair} needs a required check ID")
        if not text(entry.get("test_ref")):
            errors.append(f"traceability: {pair} needs a test/acceptance reference")
        if not text(entry.get("doc_ref")) and not text(entry.get("docs_not_applicable_reason")):
            errors.append(f"traceability: {pair} needs documentation or a specific exemption reason")
    for pair in sorted(expected_pairs - covered):
        errors.append(f"traceability: missing required scenario {pair}")

    receipt("code_review", packet.get("code_review"), independent=True)
    receipt("documentation", packet.get("documentation"))
    security = packet.get("security")
    if not isinstance(security, dict):
        errors.append("security: missing triage")
        security = {}
    if security.get("candidate") != expected_candidate:
        errors.append("security: stale or missing triage candidate")
    if security.get("triage") != "complete":
        errors.append("security: unknown or incomplete impact blocks readiness")
    if not text(security.get("rationale")):
        errors.append("security: missing applicability rationale")
    triggers = security.get("triggers")
    if not isinstance(triggers, list) or not all(text(t) for t in triggers):
        errors.append("security: triggers must be a list of risk descriptions")
        triggers = ["unknown"]
    if policy.get("security_required") is not False or triggers:
        receipt("security_review", security.get("review"), independent=True)

    sync = packet.get("spec_sync")
    if not isinstance(sync, dict):
        errors.append("spec_sync: missing result")
        sync = {}
    count = sync.get("delta_count")
    if type(count) is not int or count < 0:
        errors.append("spec_sync: delta_count must be a nonnegative integer")
        count = 1
    if policy.get("spec_sync_required") is not False or count:
        receipt("spec_sync", sync, statuses=("verified",))
        if type(sync.get("remaining_deltas")) is not int or sync["remaining_deltas"] != 0:
            errors.append("spec_sync: unapplied or unknown deltas remain")
        if sync.get("idempotent") is not True:
            errors.append("spec_sync: a clean second comparison is required")
    else:
        receipt("spec_sync", sync, statuses=("not_applicable", "verified"))
        if sync.get("status") == "not_applicable" and not text(sync.get("reason")):
            errors.append("spec_sync: not-applicable requires a reason")

    findings = packet.get("findings")
    if not isinstance(findings, list):
        errors.append("packet: findings must be an array")
        findings = []
    for finding in findings:
        if not isinstance(finding, dict) or not text(finding.get("id")):
            errors.append("findings: invalid finding record")
            continue
        if finding.get("severity") not in ("blocker", "major", "minor") or finding.get("status") not in ("open", "closed"):
            errors.append(f"finding {finding['id']}: unknown severity or status")
        elif finding["severity"] in ("blocker", "major") and finding["status"] != "closed":
            errors.append(f"finding {finding['id']}: unresolved material finding")
        if finding.get("status") == "closed" and not text(finding.get("closure_evidence")):
            errors.append(f"finding {finding['id']}: closure evidence required")

    correction = packet.get("correction")
    if not isinstance(correction, dict):
        errors.append("correction: missing persistent attempt summary")
        correction = {}
    rounds = correction.get("failed_rounds")
    if type(rounds) is not int or rounds < 0 or (rounds > 0 and rounds >= limit):
        errors.append("correction: invalid or reached failed-round stop limit")
    if correction.get("stalled") is not False:
        errors.append("correction: stalled or unknown progress")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--policy", type=Path, required=True)
    parser.add_argument("--packet", type=Path, required=True)
    parser.add_argument("--expected-candidate", required=True)
    parser.add_argument("--allow-synthetic", action="store_true", help="Fixture demonstration only")
    args = parser.parse_args()
    try:
        policy = json.loads(args.policy.read_text(encoding="utf-8"))
        packet = json.loads(args.packet.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(f"INVALID INPUT: {exc}", file=sys.stderr)
        return 2
    errors = check(policy, packet, args.expected_candidate, args.allow_synthetic)
    if errors:
        for error in errors:
            print(f"NOT READY: {error}", file=sys.stderr)
        return 1
    print("PASS: supplied packet is structurally consistent for the expected candidate.")
    print("This does not verify evidence truth, execute tests, or authorize merge/deployment.")
    if args.allow_synthetic:
        print("Synthetic fixture mode is enabled; this is not live readiness evidence.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

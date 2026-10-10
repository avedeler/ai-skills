# Bundled upstream skill

**using-git-worktrees** comes from **Superpowers**, created by **Jesse Vincent
(obra)**. Copyright (c) 2025 Jesse Vincent. Used under the [MIT License](LICENSE).
We did not author the upstream skill.

- [Original source at the pinned revision](https://github.com/obra/superpowers/blob/bb92a77741419a4ab5f06e711a283343f1ada0c3/skills/using-git-worktrees/SKILL.md)
- [Upstream license at the same revision](https://github.com/obra/superpowers/blob/bb92a77741419a4ab5f06e711a283343f1ada0c3/LICENSE)
- [Unmodified local skill](SKILL.md)
- [Provenance and SHA-256 hashes](UPSTREAM.json)

Read [the team's integration guide](../../references/worktrees.md) before applying
the source instructions. It adapts workspace ownership, fallback, setup, baseline
handling, and cleanup to a portable multi-role team. The upstream files remain
byte-for-byte unchanged. The host does not need to install Superpowers or discover
this nested directory as a separate skill; the coordinator loads it as a bundled
reference. No network fetch is required at runtime.

When updating, review an explicit upstream revision, compare its instructions and
license, replace both imported files, update hashes/provenance and notices, then
revalidate the package and behavior scenarios. Do not follow upstream `main`
automatically. Preserve this notice and the full license with redistributed copies.

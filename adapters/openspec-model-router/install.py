#!/usr/bin/env python3
"""Install canonical router plus optional Codex settings; never overwrite edits."""
import argparse
from pathlib import Path
import shutil
import tempfile


def install(skills_dir: Path) -> Path:
    adapter = Path(__file__).resolve().parent
    source = adapter.parents[1] / 'skills' / 'openspec-model-router'
    destination = skills_dir.expanduser() / source.name
    files = {p.relative_to(source): p for p in source.rglob('*') if p.is_file()}
    for name in ('model-profile.md', 'runtime.md', 'research.md'):
        files[Path('references') / name] = adapter / name
    if any(p.is_symlink() for p in (destination, *destination.parents)):
        raise ValueError('Refusing a symlink destination')
    if destination.exists():
        existing = {p.relative_to(destination) for p in destination.rglob('*') if p.is_file()}
        if (any(p.is_symlink() for p in destination.rglob('*'))
                or existing != set(files)
                or any((destination / rel).read_bytes() != src.read_bytes()
                       for rel, src in files.items())):
            raise ValueError(f'Existing installation differs; preserve and merge it manually: {destination}')
        return destination
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.router-install-', dir=destination.parent) as temp:
        staged = Path(temp) / source.name
        for rel, src in files.items():
            target = staged / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, target)
        staged.rename(destination)
    return destination


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--skills-dir', type=Path, default=Path.home() / '.agents' / 'skills')
    args = parser.parse_args()
    try:
        print(f'Installed or verified: {install(args.skills_dir)}')
    except (OSError, ValueError) as exc:
        parser.exit(1, f'{exc}\n')

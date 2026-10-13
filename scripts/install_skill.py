"""Install this checkout, backing up an existing skill before an explicit update."""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path


def payload(source: Path):
    source = source.resolve()
    text = (source / "SKILL.md").read_text(encoding="utf-8-sig")
    match = re.search(r"^name: ([a-z0-9]+(?:-[a-z0-9]+)*)\s*$", text, re.M)
    if not match:
        raise ValueError("Cannot read skill name from SKILL.md")
    files = [source / "SKILL.md"]
    if (source / "LICENSE").is_file():
        files.append(source / "LICENSE")
    for folder in ("agents", "references", "assets"):
        files.extend(p for p in sorted((source / folder).rglob("*")) if p.is_file())
    for path in files:
        if not path.resolve().is_relative_to(source):
            raise ValueError(f"Source file outside checkout: {path}")
    return match.group(1), files


def differences(source: Path, target: Path) -> list[str]:
    source = source.resolve()
    _, files = payload(source)
    return [str(path.relative_to(source)) for path in files
            if not (target / path.relative_to(source)).is_file()
            or path.read_bytes() != (target / path.relative_to(source)).read_bytes()]


def install(source: Path, target: Path, *, update=False, backup_dir=None):
    source = source.resolve()
    name, files = payload(source)
    if target.is_symlink():
        raise ValueError("Installation target cannot be a symbolic link")
    target = target.resolve()
    if target.name != name:
        raise ValueError(f"Installation directory must be named {name}")
    if target.is_relative_to(source) or source.is_relative_to(target):
        raise ValueError("Installation and source directories must not overlap")
    if target.exists() and not update:
        raise FileExistsError("Skill already exists; use --update to back it up and update")
    if target.exists() and not (target / "SKILL.md").is_file():
        raise ValueError("Existing target is not a skill directory")
    for path in files:
        output = target / path.relative_to(source)
        if output.is_symlink() or not output.resolve().is_relative_to(target):
            raise ValueError(f"Destination file escapes installation: {output}")
        if output.exists() and not output.is_file():
            raise ValueError(f"Destination is not a file: {output}")
    record = target / "INSTALLATION.json"
    if record.is_symlink() or (record.exists() and not record.is_file()):
        raise ValueError("Invalid installation record destination")

    backup = None
    if target.exists():
        base = Path(backup_dir).resolve() if backup_dir else target.parent.parent / "skill-backups"
        if base.is_relative_to(target) or base.is_relative_to(source):
            raise ValueError("Backup directory must be outside installation and checkout")
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        backup = base / name / stamp
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(target, backup, symlinks=True)

    target.mkdir(parents=True, exist_ok=True)
    for path in files:
        output = target / path.relative_to(source)
        output.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, output)

    commit, dirty = None, None
    if (source / ".git").exists():
        try:
            result = subprocess.run(["git", "rev-parse", "HEAD"], cwd=source,
                                    capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                commit = result.stdout.strip()
                status = subprocess.run(["git", "status", "--porcelain"], cwd=source,
                                        capture_output=True, text=True, timeout=5)
                if status.returncode == 0:
                    dirty = bool(status.stdout.strip())
        except (OSError, subprocess.TimeoutExpired):
            pass
    record.write_text(json.dumps({
        "skill_name": name,
        "installed_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_commit": commit,
        "source_dirty": dirty,
        "files": {str(p.relative_to(source)).replace("\\", "/"): hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in files},
    }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return backup


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--target", type=Path, help="complete installation directory, including skill name")
    parser.add_argument("--update", action="store_true")
    parser.add_argument("--backup-dir", type=Path)
    parser.add_argument("--check", action="store_true", help="compare installed skill files with this checkout")
    args = parser.parse_args()
    source = args.source.resolve()
    try:
        name, _ = payload(source)
        codex_directory = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
        target = args.target or codex_directory / "skills" / name
        if args.check:
            changed = differences(source, target.resolve())
            if changed:
                parser.exit(1, "Installed files differ: " + ", ".join(changed) + "\n")
            print("Installed skill files match this checkout.")
            return
        backup = install(source, target, update=args.update, backup_dir=args.backup_dir)
        print(f"Installed: {target.resolve()}")
        if backup:
            print(f"Previous version backup: {backup}")
        print("The updated skill will be available on your next turn.")
    except (OSError, ValueError) as exc:
        parser.exit(1, str(exc) + "\n")


if __name__ == "__main__":
    main()

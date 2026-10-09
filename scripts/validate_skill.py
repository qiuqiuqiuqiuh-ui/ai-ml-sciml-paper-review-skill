"""Validate skill metadata and local resource references; not review quality."""
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml


def validate(root: Path) -> list[str]:
    root = root.resolve()
    errors = []
    skill = root / "SKILL.md"
    if not skill.is_file():
        return ["SKILL.md is missing"]
    text = skill.read_text(encoding="utf-8-sig")
    match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)", text, re.S)
    if not match:
        return ["SKILL.md requires YAML frontmatter"]
    try:
        meta = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        return [f"Invalid frontmatter: {exc}"]
    if not isinstance(meta, dict):
        return ["Frontmatter must be a mapping"]
    name = meta.get("name")
    if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
        errors.append("Invalid skill name")
    elif name != root.name:
        errors.append("Skill name must match directory name")
    description = meta.get("description")
    if not isinstance(description, str) or not description.strip() or len(description) > 1024:
        errors.append("Description must contain 1-1024 characters")
    allowed = {"name", "description", "license", "allowed-tools", "metadata"}
    if set(meta) - allowed:
        errors.append("Unsupported frontmatter fields: " + ", ".join(sorted(set(meta) - allowed)))

    def check_path(source: Path, value: str, relative_to: Path):
        target = (relative_to / unquote(urlsplit(value).path)).resolve()
        if not target.is_relative_to(root):
            errors.append(f"{source.relative_to(root)}: resource outside skill: {value}")
        elif not target.is_file():
            errors.append(f"{source.relative_to(root)}: missing resource: {value}")

    for source in [skill, *sorted((root / "references").glob("*.md"))]:
        for value in re.findall(r"\[[^\]]*\]\(([^\s)]+)\)", source.read_text(encoding="utf-8-sig")):
            parsed = urlsplit(value)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            check_path(source, value, source.parent)

    agent = root / "agents" / "openai.yaml"
    if agent.exists():
        try:
            data = yaml.safe_load(agent.read_text(encoding="utf-8-sig"))
            if not isinstance(data, dict) or not isinstance(data.get("interface"), dict):
                errors.append("agents/openai.yaml requires an interface mapping")
            else:
                interface = data["interface"]
                for field in ("display_name", "short_description", "default_prompt"):
                    if not isinstance(interface.get(field), str) or not interface[field].strip():
                        errors.append(f"Invalid interface.{field}")
                prompt = interface.get("default_prompt", "")
                if isinstance(prompt, str) and isinstance(name, str) and f"${name}" not in prompt:
                    errors.append("default_prompt must mention the skill")
                blurb = interface.get("short_description", "")
                if isinstance(blurb, str) and not 25 <= len(blurb) <= 64:
                    errors.append("short_description must contain 25-64 characters")
                for field in ("icon_small", "icon_large"):
                    value = interface.get(field)
                    if value is not None:
                        if not isinstance(value, str):
                            errors.append(f"Invalid interface.{field}")
                        else:
                            check_path(agent, value, root)
                policy = data.get("policy", {})
                if not isinstance(policy, dict):
                    errors.append("policy must be a mapping")
                elif "allow_implicit_invocation" in policy and not isinstance(policy["allow_implicit_invocation"], bool):
                    errors.append("allow_implicit_invocation must be a boolean")
        except yaml.YAMLError as exc:
            errors.append(f"Invalid agents/openai.yaml: {exc}")
    return errors


if __name__ == "__main__":
    if len(sys.argv) > 2:
        sys.exit("Usage: python scripts/validate_skill.py [skill-directory]")
    problems = validate(Path(sys.argv[1]) if len(sys.argv) == 2 else Path(__file__).resolve().parents[1])
    if problems:
        print("\n".join(problems))
        sys.exit(1)
    print("Skill structure and local resource references are valid.")

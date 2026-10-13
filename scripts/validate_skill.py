"""Validate skill packaging and Markdown links; not scientific review quality."""
import argparse
import re
import unicodedata
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml
from markdown_it import MarkdownIt


MARKDOWN = MarkdownIt("commonmark").enable("table")


def heading_ids(tokens) -> set[str]:
    """Generate IDs for ordinary Markdown headings, including duplicate headings."""
    used = set()
    for index, token in enumerate(tokens):
        if token.type != "heading_open":
            continue
        children = tokens[index + 1].children or []
        text = "".join(t.content for t in children if t.type in {"text", "code_inline"})
        slug = "".join(
            char for char in text.lower()
            if char in " _-" or unicodedata.category(char)[0] in "LNM"
        ).replace(" ", "-")
        candidate, count = slug, 0
        while candidate in used:
            count += 1
            candidate = f"{slug}-{count}"
        used.add(candidate)
    return used


def validate(root: Path, *, check_directory_name: bool = False) -> list[str]:
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
    elif check_directory_name and name != root.name:
        errors.append("Skill name must match directory name")
    description = meta.get("description")
    if not isinstance(description, str) or not description.strip() or len(description) > 1024:
        errors.append("Description must contain 1-1024 characters")
    elif description.startswith("[TODO:") or "<" in description or ">" in description:
        errors.append("Description contains a placeholder or angle brackets")
    allowed = {"name", "description", "license", "allowed-tools", "metadata"}
    if set(meta) - allowed:
        errors.append("Unsupported frontmatter fields: " + ", ".join(sorted(set(meta) - allowed)))

    parsed_docs = {}

    def parse_doc(path: Path):
        if path not in parsed_docs:
            document = path.read_text(encoding="utf-8-sig")
            if path == skill:
                document = document[match.end():]
            parsed_docs[path] = MARKDOWN.parse(document)
        return parsed_docs[path]

    def check_path(source: Path, value: str, relative_to: Path):
        parsed = urlsplit(value)
        target = (relative_to / unquote(parsed.path)).resolve() if parsed.path else source
        if not target.is_relative_to(root):
            errors.append(f"{source.relative_to(root)}: resource outside skill: {value}")
        elif not target.is_file():
            errors.append(f"{source.relative_to(root)}: missing resource: {value}")
        elif parsed.fragment and target.suffix.lower() == ".md":
            if unquote(parsed.fragment) not in heading_ids(parse_doc(target)):
                errors.append(f"{source.relative_to(root)}: missing heading: {value}")

    ignored = {".git", ".venv", "__pycache__", ".local-backups"}
    for source in sorted(root.rglob("*.md")):
        if ignored.intersection(source.relative_to(root).parts):
            continue
        if not source.resolve().is_relative_to(root):
            errors.append(f"Resource outside skill: {source.relative_to(root)}")
            continue
        tokens = parse_doc(source)
        for token in tokens:
            if token.type == "inline":
                for line in token.content.splitlines():
                    if re.fullmatch(r"\s*\[TODO:[^\n]*\]\s*", line):
                        errors.append(f"{source.relative_to(root)}: unfinished TODO placeholder")
                for child in token.children or []:
                    if child.type not in {"link_open", "image"}:
                        continue
                    value = child.attrGet("href" if child.type == "link_open" else "src")
                    parsed = urlsplit(value)
                    if parsed.scheme or parsed.netloc:
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
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--installed", action="store_true", help="also require installation directory to match skill name")
    args = parser.parse_args()
    problems = validate(args.directory, check_directory_name=args.installed)
    if problems:
        print("\n".join(problems))
        raise SystemExit(1)
    print("Skill metadata, local resources, Markdown headings, and scaffolds are valid.")

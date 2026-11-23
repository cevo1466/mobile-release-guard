#!/usr/bin/env python3
"""Structural validator for the mobile-release-guard skill (stdlib only)."""
import pathlib
import re
import sys

MAX_SKILL_LINES = 200
ID_FILES = {
    "SEC": ("references/security-controls.md", 26),
    "APP": ("references/appstore-review.md", 24),
}


def _frontmatter(text):
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    fields = {}
    for line in text[4:end].splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            fields[k.strip()] = v.strip()
    return fields


def validate(skill_dir):
    skill_dir = pathlib.Path(skill_dir).resolve()
    errors = []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return ["SKILL.md missing"]
    text = skill_md.read_text(encoding="utf-8")

    fm = _frontmatter(text)
    if fm is None:
        errors.append("SKILL.md frontmatter missing or unterminated")
    else:
        if fm.get("name") != skill_dir.name:
            errors.append(f"frontmatter name {fm.get('name')!r} != dir {skill_dir.name!r}")
        if not fm.get("description"):
            errors.append("frontmatter description missing")
        if fm.get("disable-model-invocation") != "true":
            errors.append("disable-model-invocation must be true")

    if len(text.splitlines()) > MAX_SKILL_LINES:
        errors.append(f"SKILL.md exceeds {MAX_SKILL_LINES} lines")

    for target in re.findall(r"\]\((references/[^)#]+)\)", text):
        if not (skill_dir / target).is_file():
            errors.append(f"dangling reference link: {target}")

    for prefix, (rel, count) in ID_FILES.items():
        path = skill_dir / rel
        if not path.is_file():
            errors.append(f"missing reference file: {rel}")
            continue
        body = path.read_text(encoding="utf-8")
        for i in range(1, count + 1):
            cid = f"{prefix}-{i:02d}"
            if not re.search(rf"^## {cid}\b", body, re.M):
                errors.append(f"{cid} heading missing in {rel}")
    return errors


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: validate_skill.py <skill_dir>", file=sys.stderr)
        sys.exit(2)
    problems = validate(sys.argv[1])
    for p in problems:
        print(f"FAIL: {p}")
    if not problems:
        print("OK")
    sys.exit(1 if problems else 0)

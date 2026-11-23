#!/usr/bin/env python3
"""Structural validator for the mobile-release-guard skill (stdlib only)."""
import os
import pathlib
import re
import sys

MAX_SKILL_LINES = 200
ID_FILES = {  # heading style: "## SEC-01 — title"
    "SEC": ("references/security-controls.md", 26),
    "APP": ("references/appstore-review.md", 24),
    "GP": ("references/google-play-review.md", 25),
}
ROW_FILES = {  # table-row style: "| EXT-01 | ..."
    "EXT": ("references/owasp-extras.md", 21),
    "AI": ("references/owasp-extras.md", 19),
}
OFFICIAL_URLS = [
    "https://code.claude.com/docs/en/skills",
    "https://claude.com/plugins/skill-creator",
    "https://developer.apple.com/app-store/review/guidelines/",
    "https://developer.apple.com/documentation/",
    "https://developer.apple.com/app-store/review/",
    "https://support.apple.com/guide/security/welcome/web",
    "https://developer.android.com/",
    "https://play.google.com/about/developer-content-policy/",
    "https://support.google.com/googleplay/android-developer/",
    "https://mas.owasp.org/MASVS/",
    "https://mas.owasp.org/MASTG/",
    "https://owasp.org/API-Security/",
    "https://firebase.google.com/docs",
    "https://supabase.com/docs",
    "https://www.swift.org/documentation/",
    "https://docs.flutter.dev/",
    "https://reactnative.dev/docs/getting-started",
]


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

    for prefix, (rel, count) in ROW_FILES.items():
        path = skill_dir / rel
        if not path.is_file():
            errors.append(f"missing reference file: {rel}")
            continue
        body = path.read_text(encoding="utf-8")
        for i in range(1, count + 1):
            cid = f"{prefix}-{i:02d}"
            if not re.search(rf"^\|\s*{cid}\s*\|", body, re.M):
                errors.append(f"{cid} row missing in {rel}")

    tpl = skill_dir / "references/report-template.md"
    if tpl.is_file():
        body = tpl.read_text(encoding="utf-8")
        for letter in "ABCDEFGHIJKL":
            if f"**{letter}." not in body:
                errors.append(f"report section {letter} missing in report-template.md")
    else:
        errors.append("missing reference file: references/report-template.md")

    src = skill_dir / "references/official-sources.md"
    if src.is_file():
        body = src.read_text(encoding="utf-8")
        for url in OFFICIAL_URLS:
            if url not in body:
                errors.append(f"official source missing: {url}")
    else:
        errors.append("missing reference file: references/official-sources.md")

    evals = skill_dir / "evals"
    if evals.is_dir():
        if (evals / "evals.json").exists():
            errors.append("evals/evals.json must not coexist with case folders")
        for case in sorted(p for p in evals.iterdir() if p.is_dir()):
            if not (case / "prompt.md").is_file() or not (case / "case.yaml").is_file():
                errors.append(f"eval case {case.name}: prompt.md or case.yaml missing")
            if not list((case / "graders").glob("*.md")):
                errors.append(f"eval case {case.name}: no graders/*.md")

    for sh in sorted((skill_dir / "scripts").glob("*.sh")):
        if not os.access(sh, os.X_OK):
            errors.append(f"script not executable: scripts/{sh.name}")
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

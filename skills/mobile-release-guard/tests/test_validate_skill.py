import os
import pathlib
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "scripts"))
import validate_skill  # noqa: E402
from validate_skill import validate  # noqa: E402

FRONTMATTER = (
    "---\nname: {name}\ndescription: test skill\n"
    "disable-model-invocation: true\n---\n"
)


def make_skill(root, drop_sec=None, dangling=False, drop_gp=None, drop_ext=None, drop_ai=None,
               drop_url=None, drop_section=None, case_without_graders=False, non_exec=False,
               old_evals_json=False):
    d = pathlib.Path(root) / "mobile-release-guard"
    ref = d / "references"
    ref.mkdir(parents=True)
    links = "[a](references/security-controls.md) [b](references/appstore-review.md)"
    if dangling:
        links += " [c](references/missing.md)"
    (d / "SKILL.md").write_text(FRONTMATTER.format(name=d.name) + links + "\n")
    heads = lambda p, n, drop: "".join(f"## {p}-{i:02d} — x\n" for i in range(1, n + 1) if i != drop)
    rows = lambda p, n, drop: "".join(f"| {p}-{i:02d} | x |\n" for i in range(1, n + 1) if i != drop)
    (ref / "security-controls.md").write_text(heads("SEC", 26, drop_sec))
    (ref / "appstore-review.md").write_text(heads("APP", 24, None))
    (ref / "google-play-review.md").write_text(heads("GP", 25, drop_gp))
    (ref / "owasp-extras.md").write_text(rows("EXT", 21, drop_ext) + rows("AI", 19, drop_ai))
    (ref / "report-template.md").write_text("".join(
        f"- **{c}. Bölüm**\n" for c in "ABCDEFGHIJKL" if c != drop_section))
    (ref / "official-sources.md").write_text("".join(
        f"- {u}\n" for u in validate_skill.OFFICIAL_URLS if u != drop_url))
    case = d / "evals" / "case-a"
    (case / "graders").mkdir(parents=True)
    (case / "prompt.md").write_text("---\ntags: [x]\n---\n\n/mobile-release-guard audit\n")
    (case / "case.yaml").write_text('schema_version: "1.1"\nname: case-a\nexpected_outcome: |\n  x\n')
    if not case_without_graders:
        (case / "graders" / "01-x.md").write_text("---\ntype: llm\nfocus: trace\nweight: 1\n---\n\nx\n")
    if old_evals_json:
        (d / "evals" / "evals.json").write_text("{}")
    sh = d / "scripts" / "tool.sh"
    sh.parent.mkdir()
    sh.write_text("#!/usr/bin/env bash\n")
    os.chmod(sh, 0o644 if non_exec else 0o755)
    return d


def msgs(**kw):
    with tempfile.TemporaryDirectory() as t:
        return validate(make_skill(t, **kw))


class ValidateTests(unittest.TestCase):
    def test_missing_skill_md_fails(self):
        with tempfile.TemporaryDirectory() as t:
            d = pathlib.Path(t) / "mobile-release-guard"
            d.mkdir()
            self.assertTrue(validate(d))

    def test_complete_fixture_passes(self):
        self.assertEqual(msgs(), [])

    def test_missing_sec_id_reported(self):
        self.assertTrue(any("SEC-26" in m for m in msgs(drop_sec=26)))

    def test_dangling_reference_link_reported(self):
        self.assertTrue(any("missing.md" in m for m in msgs(dangling=True)))

    def test_missing_gp_id_reported(self):
        self.assertTrue(any("GP-25" in m for m in msgs(drop_gp=25)))

    def test_missing_ext_id_reported(self):
        self.assertTrue(any("EXT-21" in m for m in msgs(drop_ext=21)))

    def test_missing_ai_id_reported(self):
        self.assertTrue(any("AI-19" in m for m in msgs(drop_ai=19)))

    def test_missing_report_section_reported(self):
        self.assertTrue(any("section L" in m for m in msgs(drop_section="L")))

    def test_missing_official_url_reported(self):
        url = validate_skill.OFFICIAL_URLS[0]
        self.assertTrue(any(url in m for m in msgs(drop_url=url)))
        self.assertEqual(len(validate_skill.OFFICIAL_URLS), 17)

    def test_case_without_graders_reported(self):
        self.assertTrue(any("case-a" in m and "graders" in m for m in msgs(case_without_graders=True)))

    def test_non_executable_script_reported(self):
        self.assertTrue(any("tool.sh" in m and "executable" in m for m in msgs(non_exec=True)))

    def test_old_evals_json_reported(self):
        self.assertTrue(any("evals.json" in m for m in msgs(old_evals_json=True)))


if __name__ == "__main__":
    unittest.main()

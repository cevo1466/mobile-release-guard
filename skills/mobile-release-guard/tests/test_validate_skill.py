import pathlib
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "scripts"))
from validate_skill import validate  # noqa: E402

FRONTMATTER = (
    "---\nname: {name}\ndescription: test skill\n"
    "disable-model-invocation: true\n---\n"
)


def make_skill(root, drop_sec=None, dangling=False):
    d = pathlib.Path(root) / "mobile-release-guard"
    (d / "references").mkdir(parents=True)
    links = "[a](references/security-controls.md) [b](references/appstore-review.md)"
    if dangling:
        links += " [c](references/missing.md)"
    (d / "SKILL.md").write_text(FRONTMATTER.format(name=d.name) + links + "\n")
    sec = "".join(f"## SEC-{i:02d} — x\n" for i in range(1, 27) if i != drop_sec)
    app = "".join(f"## APP-{i:02d} — x\n" for i in range(1, 25))
    (d / "references/security-controls.md").write_text(sec)
    (d / "references/appstore-review.md").write_text(app)
    return d


class ValidateTests(unittest.TestCase):
    def test_missing_skill_md_fails(self):
        with tempfile.TemporaryDirectory() as t:
            d = pathlib.Path(t) / "mobile-release-guard"
            d.mkdir()
            self.assertTrue(validate(d))

    def test_missing_sec_id_reported(self):
        with tempfile.TemporaryDirectory() as t:
            d = make_skill(t, drop_sec=26)
            self.assertTrue(any("SEC-26" in m for m in validate(d)))

    def test_dangling_reference_link_reported(self):
        with tempfile.TemporaryDirectory() as t:
            d = make_skill(t, dangling=True)
            self.assertTrue(any("missing.md" in m for m in validate(d)))

    def test_complete_fixture_passes(self):
        with tempfile.TemporaryDirectory() as t:
            d = make_skill(t)
            self.assertEqual(validate(d), [])


if __name__ == "__main__":
    unittest.main()

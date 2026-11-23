"""Static trace of evals/evals.json: every expected behavior must be backed by a concrete
rule in the skill text or by a script that really runs. This is NOT a live model run."""
import pathlib
import re
import subprocess
import tempfile
import unittest

SKILL = pathlib.Path(__file__).resolve().parent.parent


def txt(p):
    return (SKILL / p).read_text(encoding="utf-8").replace("İ", "I").lower()


def section(path, ident):
    body = (SKILL / path).read_text(encoding="utf-8")
    m = re.search(rf"(?ms)^## {ident}\b.*?(?=^## |\Z)", body)
    assert m, f"{ident} missing in {path}"
    return m.group(0).lower()


def run(script, arg):
    return subprocess.run(["bash", str(SKILL / "scripts" / script), str(arg)],
                          capture_output=True, text=True)


class EvalTrace(unittest.TestCase):
    def test_offline_app_not_applicable_conditions(self):
        for i in (3, 4, 6, 8, 9, 10, 11, 13, 24, 25, 26):
            s = section("references/security-controls.md", f"SEC-{i:02d}")
            self.assertIn("koşul", s, f"SEC-{i:02d} has no applicability condition")
        for i in (8, 9, 10, 11, 13, 14, 24):
            s = section("references/appstore-review.md", f"APP-{i:02d}")
            self.assertIn("not_applicable", s, f"APP-{i:02d} lacks explicit NOT_APPLICABLE")
        offline = run("detect_stack.sh", SKILL / "evals/fixtures/offline-ios").stdout.split()
        self.assertNotIn("firebase", offline)
        self.assertNotIn("storekit", offline)

    def test_android_does_not_require_ios_rules(self):
        s = txt("SKILL.md")
        self.assertRegex(s, r"app store.*ios|ios.*app store")
        self.assertIn("android-only", s + txt("references/report-template.md"))

    def test_no_mobile_project_detected(self):
        s = txt("SKILL.md")
        self.assertRegex(s, r"mobil proje algılanmazsa|mobil proje bulunamazsa")
        with tempfile.TemporaryDirectory() as t:
            out = run("detect_stack.sh", t)
            self.assertEqual(out.returncode, 0)
            self.assertEqual(out.stdout.strip(), "")
            self.assertEqual(run("scan_secrets.sh", t).stdout.strip(), "")

    def test_unverified_without_backend(self):
        s = txt("SKILL.md") + txt("references/security-controls.md")
        self.assertIn("unverified", s)
        self.assertRegex(s, r"backend.*erişim.*unverified|unverified.*backend")

    def test_linux_ios_rule(self):
        t = txt("references/testing-strategy.md")
        self.assertIn("çalıştırılamadı", t)
        self.assertIn("kurma", txt("SKILL.md"))

    def test_prompt_injection_rule(self):
        s = txt("SKILL.md")
        self.assertIn("güvenilmeyen veri", s)
        self.assertIn("şüpheli", s)
        self.assertNotIn("curl", s)  # the skill itself must not embed such commands

    def test_bad_argument_rule(self):
        s = txt("SKILL.md")
        self.assertIn("tanınmayan", s)
        self.assertIn("sor", s)

    def test_public_ids_not_secrets(self):
        s = txt("references/security-controls.md")
        self.assertIn("anon", s)
        self.assertIn("secret değildir", s)

    def test_app_check_not_authz(self):
        self.assertIn("yerine geçmez", section("references/security-controls.md", "SEC-13"))

    def test_fix_policy_mechanisms(self):
        r = txt("references/remediation-policy.md")
        for kw in ["git status", "git diff", "onay", "testi kapatarak"]:
            self.assertIn(kw, r)

    def test_stale_rules(self):
        g = txt("references/google-play-review.md")
        self.assertIn("doğrulanamazsa unverified", g)
        self.assertIn("sayı uydurma", g)

    def test_scan_secrets_never_prints_values_and_finds_seeded_keys(self):
        for fx in ("swiftui-firebase-storekit2", "ai-subscription"):
            out = run("scan_secrets.sh", SKILL / "evals/fixtures" / fx)
            self.assertIn("HARDCODED_SECRET", out.stdout, fx)
            self.assertNotRegex(out.stdout + out.stderr, r"FAKE_\w*DO_NOT_PRINT")
        self.assertEqual(run("scan_secrets.sh", SKILL / "evals/fixtures/offline-ios").stdout.strip(), "")


if __name__ == "__main__":
    unittest.main()

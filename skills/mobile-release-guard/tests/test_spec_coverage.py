"""Checks the installed skill against writing-block.md requirements (section numbers = spec sections)."""
import json
import pathlib
import re
import subprocess
import unittest

SKILL = pathlib.Path(__file__).resolve().parent.parent
REF = SKILL / "references"


CASE = {"swiftui-firebase-storekit2": "swiftui-firebase-storekit2", "kotlin-compose-billing": "kotlin-compose-billing",
        "flutter-firebase": "flutter-firebase-rules", "rn-supabase": "rn-supabase-rls",
        "ai-subscription": "ai-subscription", "offline-ios": "offline-app"}


def read(p):
    return (SKILL / p).read_text(encoding="utf-8")


def low(p):
    return read(p).replace("İ", "I").lower()


class Spec(unittest.TestCase):
    # ---- §4 modes and arguments
    def test_modes_and_arguments(self):
        s = read("SKILL.md")
        self.assertIn("$ARGUMENTS", s)
        for tok in ["audit", "plan", "fix", "verify", "ios", "android", "all", "security",
                    "appstore", "googleplay", "subscriptions", "critical"]:
            self.assertRegex(s, rf"\b{tok}\b", tok)
        self.assertRegex(s.lower(), r"sessizce")  # unknown args never silently ignored
        self.assertIn("disable-model-invocation: true", s)

    # ---- §6 statuses, §16 verdicts and sections, priorities
    def test_statuses_verdicts_sections(self):
        blob = read("SKILL.md") + read("references/report-template.md")
        for t in ["PASS", "FAIL", "PARTIAL", "NOT_APPLICABLE", "UNVERIFIED", "BLOCKED", "NEEDS_WORK",
                  "READY_WITH_CAVEATS", "READY_BASED_ON_VERIFIED_SCOPE", "P0", "P1", "P2", "P3"]:
            self.assertIn(t, blob, t)
        for letter in "ABCDEFGHIJKL":
            self.assertRegex(read("references/report-template.md"), rf"\*\*{letter}\. ", letter)
        for field in ["Kanıt", "Etki", "Düzeltme", "Test", "Uygulanabilirlik", "Risk"]:
            self.assertIn(field, read("references/report-template.md"), field)

    # ---- §9 Google Play
    def test_google_play_ids_and_topics(self):
        g = read("references/google-play-review.md")
        for i in range(1, 26):
            self.assertRegex(g, rf"(?m)^## GP-{i:02d}\b", f"GP-{i:02d}")
        gl = g.lower()
        for kw in ["target", "app bundle", "signing", "billing", "acknowledg", "data safety",
                   "hesap silme", "privacy", "runtime", "sensitive", "background location",
                   "foreground", "bildirim", "backup", "app links", "play integrity",
                   "families", "sdk", "anr", "r8", "abi"]:
            self.assertIn(kw if kw != "sensitive" else "hassas izin", gl, kw)

    # ---- §10 21 supplementary controls
    def test_owasp_extras_cover_21_topics(self):
        e = low("references/owasp-extras.md")
        topics = ["sql", "nosql", "xss", "csrf", "authorization bypass", "deserialization",
                  "webview", "tls", "hardcoded", "loglama", "pii", "sdk", "veri silme",
                  "transaction", "race", "replay", "dosya yükleme", "broken authentication",
                  "authentication state", "abuse", "debug", "release build"]
        for t in topics:
            self.assertIn(t, e, t)
        ids = re.findall(r"EXT-(\d\d)", read("references/owasp-extras.md"))
        self.assertGreaterEqual(len(set(ids)), 21)

    # ---- §12 AI and subscription profile (19 items)
    def test_ai_subscription_profile(self):
        e = low("references/owasp-extras.md")
        for kw in ["llm api key", "istemciden doğrudan", "bütçe", "rate limit", "prompt injection",
                   "tool-calling", "model çıktı", "uygunsuz içerik", "hassas veri", "kesinti",
                   "kötüye kullanım", "maliyet", "plus/pro", "entitlement", "restore purchases",
                   "duplicate transaction", "webhook", "grace period", "cihaz"]:
            self.assertIn(kw, e, kw)

    # ---- §11 trust boundary, §13 fix policy, §19 untrusted content
    def test_safety_rules_present(self):
        s = low("SKILL.md")
        self.assertIn("güvenilir ortam değildir", s)
        self.assertIn("güvenilmeyen veri", s)
        r = low("references/remediation-policy.md")
        for kw in ["git status", "destructive", "onay", "production", "secret", "exception",
                   "testi kapat", "reset --hard"]:
            self.assertIn(kw if kw != "destructive" else "yıkıcı", r, kw)

    # ---- §14 test strategy per technology
    def test_testing_strategy_covers_stacks(self):
        t = low("references/testing-strategy.md")
        for kw in ["xcodebuild", "gradlew", "lint", "flutter test", "dart analyze", "tsc", "eslint",
                   "jest", "linux", "macos", "authorization", "storekit"]:
            self.assertIn(kw, t, kw)

    # ---- §17 sources
    def test_official_sources_complete(self):
        o = read("references/official-sources.md")
        urls = """https://code.claude.com/docs/en/skills
https://claude.com/plugins/skill-creator
https://developer.apple.com/app-store/review/guidelines/
https://developer.apple.com/documentation/
https://developer.apple.com/app-store/review/
https://support.apple.com/guide/security/welcome/web
https://developer.android.com/
https://play.google.com/about/developer-content-policy/
https://support.google.com/googleplay/android-developer/
https://mas.owasp.org/MASVS/
https://mas.owasp.org/MASTG/
https://owasp.org/API-Security/
https://firebase.google.com/docs
https://supabase.com/docs
https://www.swift.org/documentation/
https://docs.flutter.dev/
https://reactnative.dev/docs/getting-started""".split()
        for u in urls:
            self.assertIn(u, o, u)

    # ---- §9/§8 no hardcoded volatile numbers
    def test_no_hardcoded_policy_versions(self):
        for f in REF.glob("*.md"):
            t = f.read_text(encoding="utf-8")
            self.assertIsNone(re.search(r"(?i)target\s*sdk\s*(level\s*)?\d{2}|API\s*(level\s*)?3\d\b|Billing\s*Library\s*(v|sürüm\s*)?\d+\.\d", t), f.name)

    # ---- §20 evals (skill-creator case folders)
    def test_eval_scenarios(self):
        ev = SKILL / "evals"
        cases = sorted(d for d in ev.iterdir() if d.is_dir() and (d / "prompt.md").is_file())
        names = {d.name for d in cases}
        for pos in ["swiftui-firebase-storekit2", "kotlin-compose-billing", "flutter-firebase-rules",
                    "rn-supabase-rls", "offline-app", "ai-subscription"]:
            self.assertIn(pos, names)
        joined = " ".join(names)
        for kw in ["public-ids", "missing-repo", "backend", "linux", "tools", "fix-regression",
                   "injection", "fake", "stale", "argument"]:
            self.assertIn(kw, joined, kw)
        self.assertGreaterEqual(len(cases), 16)
        for d in cases:
            self.assertTrue((d / "case.yaml").is_file(), d.name)
            self.assertTrue(list((d / "graders").glob("*.md")), d.name)
            self.assertTrue(re.fullmatch(r"[a-z][a-z0-9-]*", d.name), d.name)
        self.assertFalse((ev / "evals.json").exists(), "old evals.json must not coexist")

    # ---- scripts behave (read-only, no secret echo)
    def test_scan_secrets_redacts(self):
        script = SKILL / "scripts" / "scan_secrets.sh"
        self.assertTrue(script.is_file(), "scan_secrets.sh missing")
        fx = SKILL / "evals" / "swiftui-firebase-storekit2" / "files"
        out = subprocess.run(["bash", str(script), str(fx)], capture_output=True, text=True)
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertNotIn("FAKE_KEY_DO_NOT_PRINT_123", out.stdout + out.stderr)
        self.assertIn("App.swift", out.stdout)

    def test_scan_secrets_ignores_public_ids_and_is_readonly(self):
        script = SKILL / "scripts" / "scan_secrets.sh"
        fx = SKILL / "evals" / "rn-supabase-rls" / "files"
        before = sorted(p.stat().st_mtime for p in fx.rglob("*") if p.is_file())
        out = subprocess.run(["bash", str(script), str(fx)], capture_output=True, text=True)
        after = sorted(p.stat().st_mtime for p in fx.rglob("*") if p.is_file())
        self.assertEqual(before, after)
        self.assertEqual(out.returncode, 0)

    def test_detect_stack_all_fixtures(self):
        expect = {"swiftui-firebase-storekit2": {"swiftui", "firebase", "storekit"},
                  "kotlin-compose-billing": {"kotlin", "compose", "play-billing"},
                  "flutter-firebase": {"flutter", "firebase", "firestore-rules"},
                  "rn-supabase": {"react-native", "supabase"},
                  "ai-subscription": {"llm-api", "storekit"},
                  "offline-ios": {"swiftui"}}
        for name, tags in expect.items():
            fx = SKILL / "evals" / CASE[name] / "files"
            out = subprocess.run(["bash", str(SKILL / "scripts" / "detect_stack.sh"), str(fx)],
                                 capture_output=True, text=True).stdout.split()
            self.assertTrue(tags <= set(out), f"{name}: {out}")
        off = subprocess.run(["bash", str(SKILL / "scripts" / "detect_stack.sh"),
                              str(SKILL / "evals" / "offline-app" / "files")],
                             capture_output=True, text=True).stdout.split()
        for forbidden in ["firebase", "supabase", "storekit", "llm-api", "revenuecat"]:
            self.assertNotIn(forbidden, off)

    def test_detect_stack_covers_spec_technologies(self):
        s = read("scripts/detect_stack.sh")
        for tag in ["objective-c", "ionic", "capacitor", "kotlin-multiplatform", "cloudflare-workers",
                    "fastapi", "nestjs", "express", "laravel", "graphql", "revenuecat", "supabase",
                    "firebase", "llm-api", "cocoapods", "swiftpm", "gradle", "expo"]:
            self.assertIn(tag, s, tag)


if __name__ == "__main__":
    unittest.main()

"""scan_secrets.sh: patterns, redaction and --strict exit codes.
Fake tokens are assembled at run time so the repository never stores realistic secret strings."""
import pathlib
import subprocess
import tempfile
import unittest

SKILL = pathlib.Path(__file__).resolve().parent.parent
SCRIPT = SKILL / "scripts" / "scan_secrets.sh"
CASES = SKILL / "evals"

STRIPE = "sk_" + "live_" + "a1B2c3D4e5F6g7H8i9J0k1L2"
GOOGLE = "AI" + "za" + "Sy" + "A" * 33
SENDGRID = "SG." + "A" * 22 + "." + "B" * 43
PRIVKEY = "-----BEGIN " + "RSA PRIVATE KEY-----"


def scan(target, *flags):
    return subprocess.run(["bash", str(SCRIPT), *flags, str(target)], capture_output=True, text=True)


def project(files):
    d = tempfile.TemporaryDirectory()
    for name, body in files.items():
        p = pathlib.Path(d.name) / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(body)
    return d


class ScannerPatterns(unittest.TestCase):
    def check(self, token, label, fname="Config.swift", body=None):
        d = project({fname: body or f'let x = "{token}"\n'})
        with d:
            out = scan(d.name)
            self.assertIn(label, out.stdout, out.stdout)
            self.assertNotIn(token, out.stdout + out.stderr)

    def test_stripe_live_key(self):
        self.check(STRIPE, "STRIPE_KEY")

    def test_google_api_key(self):
        self.check(GOOGLE, "GOOGLE_API_KEY")

    def test_sendgrid_key(self):
        self.check(SENDGRID, "SENDGRID_KEY")

    def test_private_key_block(self):
        self.check(PRIVKEY, "PRIVATE_KEY", body=PRIVKEY + "\nAAAA\n")

    def test_sensitive_file_by_name(self):
        with project({"certs/release.p12": "binary"}) as _:
            pass
        d = project({"certs/release.p12": "x"})
        with d:
            self.assertIn("SENSITIVE_FILE certs/release.p12", scan(d.name).stdout)

    def test_firebase_config_key_is_public(self):
        d = project({"GoogleService-Info.plist": f"<string>{GOOGLE}</string>\n"})
        with d:
            out = scan(d.name)
            self.assertIn("PUBLIC_CLIENT_ID GoogleService-Info.plist", out.stdout)
            self.assertNotIn("GOOGLE_API_KEY", out.stdout)
            self.assertEqual(scan(d.name, "--strict").returncode, 0)


class ScannerExitCodes(unittest.TestCase):
    def test_report_mode_always_exits_zero(self):
        self.assertEqual(scan(CASES / "ai-subscription/files").returncode, 0)

    def test_strict_fails_on_secret(self):
        out = scan(CASES / "ai-subscription/files", "--strict")
        self.assertEqual(out.returncode, 1)
        self.assertIn("HARDCODED_SECRET", out.stdout)

    def test_strict_passes_when_clean(self):
        for case in ("offline-app", "public-ids-not-secrets", "rn-supabase-rls"):
            self.assertEqual(scan(CASES / case / "files", "--strict").returncode, 0, case)

    def test_strict_ignores_public_client_id_only(self):
        out = scan(CASES / "public-ids-not-secrets/files", "--strict")
        self.assertIn("PUBLIC_CLIENT_ID", out.stdout)
        self.assertEqual(out.returncode, 0)

    def test_usage_errors_exit_two(self):
        self.assertEqual(scan("/nonexistent/dir").returncode, 2)
        self.assertEqual(subprocess.run(["bash", str(SCRIPT), "--bogus", "."], capture_output=True).returncode, 2)

    def test_strict_is_read_only(self):
        d = project({"a.swift": f'let x = "{STRIPE}"\n'})
        with d:
            before = (pathlib.Path(d.name) / "a.swift").read_bytes()
            scan(d.name, "--strict")
            self.assertEqual(before, (pathlib.Path(d.name) / "a.swift").read_bytes())


if __name__ == "__main__":
    unittest.main()

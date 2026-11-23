"""detect_stack.sh on synthetic layouts (directories, monorepos, marker-only projects)."""
import pathlib
import subprocess
import tempfile
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parent.parent / "scripts" / "detect_stack.sh"


def detect(layout):
    """layout: {relative path: content}; a path ending in '/' creates a directory."""
    with tempfile.TemporaryDirectory() as d:
        root = pathlib.Path(d)
        for rel, body in layout.items():
            p = root / rel
            if rel.endswith("/"):
                p.mkdir(parents=True, exist_ok=True)
            else:
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(body)
        out = subprocess.run(["bash", str(SCRIPT), str(root)], capture_output=True, text=True)
        assert out.returncode == 0, out.stderr
        return set(out.stdout.split())


class Detect(unittest.TestCase):
    def test_xcodeproj_is_a_directory(self):
        self.assertIn("xcode", detect({"Demo.xcodeproj/": ""}))

    def test_xcworkspace_is_a_directory(self):
        self.assertIn("xcode", detect({"Demo.xcworkspace/": ""}))

    def test_pbxproj_alone(self):
        self.assertIn("xcode", detect({"Demo.xcodeproj/project.pbxproj": "// !$*UTF8*$!"}))
        self.assertIn("xcode", detect({"ios/App/project.pbxproj": "x"}))

    def test_monorepo_mobile_and_backend(self):
        tags = detect({"apps/mobile/pubspec.yaml": "name: m\n",
                       "server/package.json": '{"dependencies":{"express":"4.0.0"}}'})
        self.assertTrue({"flutter", "express"} <= tags, tags)

    def test_settings_gradle_alone(self):
        self.assertIn("gradle", detect({"settings.gradle.kts": "rootProject.name = 'x'"}))

    def test_version_catalog_alone(self):
        self.assertIn("gradle", detect({"gradle/libs.versions.toml": "[versions]\n"}))

    def test_podfile_lock_alone(self):
        self.assertIn("cocoapods", detect({"Podfile.lock": "PODS:\n"}))

    def test_expo_via_app_json(self):
        self.assertIn("expo", detect({"app.json": '{"expo": {"name": "x"}}'}))

    def test_react_native_native_folders(self):
        tags = detect({"package.json": '{"dependencies":{"react-native":"0.74.0"}}', "ios/": "", "android/": ""})
        self.assertIn("react-native", tags)

    def test_node_modules_is_ignored(self):
        self.assertNotIn("firebase", detect({"node_modules/x/GoogleService-Info.plist": ""}))

    def test_empty_directory(self):
        self.assertEqual(detect({}), set())

    def test_no_false_positive_without_markers(self):
        tags = detect({"README.md": "mentions firebase and supabase and storekit"})
        self.assertEqual(tags, set())


if __name__ == "__main__":
    unittest.main()

import json
import subprocess
import sys
import unittest


def run_cli(*args):
    return subprocess.run(
        [sys.executable, "-m", "lunarness_fashion_data", *args],
        check=False,
        capture_output=True,
        text=True,
    )


class CliTests(unittest.TestCase):
    def test_validate_command_succeeds(self):
        result = run_cli("validate")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Dataset is valid.", result.stdout)

    def test_get_command_returns_caveat_and_source(self):
        result = run_cli("get", "eu_textile_consumption")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Apparent consumption estimate", result.stdout)
        self.assertIn("https://www.eea.europa.eu/", result.stdout)

    def test_search_command_emits_json(self):
        result = run_cli("search", "Fashion Week", "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertGreaterEqual(len(payload), 4)

    def test_unknown_record_exits_nonzero(self):
        result = run_cli("get", "missing")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Unknown record id", result.stderr)

    def test_version_matches_release(self):
        result = run_cli("--version")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "1.0.0")


if __name__ == "__main__":
    unittest.main()

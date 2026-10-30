import subprocess
import unittest
from types import SimpleNamespace
from unittest.mock import patch

import app


class TranscriberTests(unittest.TestCase):
    def test_success_escapes_html_uses_bounded_timeouts_and_cleans_tempdir(self):
        outputs = [SimpleNamespace(stdout="", stderr=""), SimpleNamespace(stdout=" <script>bad</script> ", stderr="")]
        with patch.object(app.subprocess, "run", side_effect=outputs) as run:
            response = app.transcribe("https://www.tiktok.com/@demo/video/123")
        self.assertIsInstance(response, str)
        self.assertIn("&lt;script&gt;bad&lt;/script&gt;", response)
        self.assertNotIn("<script>bad</script>", response)
        self.assertEqual([call.kwargs["timeout"] for call in run.call_args_list], [180, 600])
        audio_path = run.call_args_list[0].args[0][run.call_args_list[0].args[0].index("-o") + 1]
        self.assertFalse(__import__("os").path.exists(audio_path.rsplit("/", 1)[0]))

    def test_timeout_is_sanitized_504(self):
        with patch.object(app.subprocess, "run", side_effect=subprocess.TimeoutExpired("tool", 180, stderr="secret")):
            response = app.transcribe("https://www.tiktok.com/@demo/video/123")
        self.assertEqual(response.status_code, 504)
        self.assertNotIn("secret", response.body.decode())

    def test_process_failure_is_sanitized_502(self):
        with patch.object(app.subprocess, "run", side_effect=subprocess.CalledProcessError(1, "tool", stderr="secret")):
            response = app.transcribe("https://www.tiktok.com/@demo/video/123")
        self.assertEqual(response.status_code, 502)
        self.assertNotIn("secret", response.body.decode())

    def test_unexpected_failure_is_sanitized_500(self):
        with patch.object(app.subprocess, "run", side_effect=RuntimeError("secret")):
            response = app.transcribe("https://www.tiktok.com/@demo/video/123")
        self.assertEqual(response.status_code, 500)
        self.assertNotIn("secret", response.body.decode())


if __name__ == "__main__":
    unittest.main()

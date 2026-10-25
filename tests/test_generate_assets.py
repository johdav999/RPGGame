import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import generate_assets as assets


class GenerationTests(unittest.TestCase):
    def test_dry_run_never_uses_network_or_credentials(self):
        for arguments in (["speech", "--text", "Welcome"], ["model", "--prompt", "Stone arch"]):
            with patch.object(assets, "request") as request, patch.dict(assets.os.environ, {}, clear=True):
                with contextlib.redirect_stdout(io.StringIO()) as output:
                    self.assertEqual(assets.main(arguments + ["--dry-run"]), 0)
                self.assertIn("payload", json.loads(output.getvalue()))
                request.assert_not_called()

    def test_download_does_not_receive_api_key(self):
        task = {"status": "success", "output": {"model_url": "https://assets.example/model.glb"}}
        with patch.object(assets, "tripo_call", return_value=task), patch.object(assets, "request", return_value=b"glTFdata") as request:
            self.assertEqual(assets.wait_for_model("task_123", 5), b"glTFdata")
            request.assert_called_once_with("https://assets.example/model.glb", binary=True)

    def test_failed_task_stops_polling(self):
        with patch.object(assets, "tripo_call", return_value={"status": "failed"}) as call:
            with self.assertRaisesRegex(RuntimeError, "failed"):
                assets.wait_for_model("task_123", 5)
            call.assert_called_once()

    def test_invalid_download_and_provider_error(self):
        with patch.object(assets, "tripo_call", return_value={"status": "success", "output": {"model_url": "http://bad"}}):
            with self.assertRaisesRegex(RuntimeError, "HTTPS"):
                assets.wait_for_model("task_123", 5)
        with patch.dict(assets.os.environ, {"TRIPO_API_KEY": "test"}), patch.object(assets, "request", return_value={"code": 2010}):
            with self.assertRaisesRegex(RuntimeError, "rejected"):
                assets.tripo_call("tasks/task_123")

    def test_timeout_and_overwrite_protection(self):
        with self.assertRaisesRegex(RuntimeError, "model-result"):
            assets.wait_for_model("task_123", 0)
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "asset.mp3"
            path.write_bytes(b"original")
            with self.assertRaises(ValueError):
                assets.output_path(path, ".mp3")
            with self.assertRaises(FileExistsError):
                assets.write_asset(path, b"replacement")
            self.assertEqual(path.read_bytes(), b"original")

    def test_task_ids_cannot_inject_paths(self):
        for value in ("../account", "", "task?key=secret"):
            with self.assertRaises(ValueError):
                assets.safe_task_id(value)


if __name__ == "__main__":
    unittest.main()

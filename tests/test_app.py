from unittest.mock import patch, Mock
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_home():
    assert client.get("/").status_code == 200

def test_transcription_success():
    with patch("app.subprocess.run") as run:
        run.side_effect = [Mock(stdout=""), Mock(stdout="Hola mundo")]
        r = client.post("/", data={"url": "https://example.com/video"})
        assert r.status_code == 200
        assert "Hola mundo" in r.text
        assert run.call_count == 2

def test_transcription_escapes_html():
    with patch("app.subprocess.run") as run:
        run.side_effect = [Mock(stdout=""), Mock(stdout="<script>alert(1)</script>")]
        r = client.post("/", data={"url": "https://example.com/video"})
        assert "<script>" not in r.text
        assert "&lt;script&gt;" in r.text

def test_download_failure():
    import subprocess
    with patch("app.subprocess.run", side_effect=subprocess.CalledProcessError(1, "yt-dlp")):
        assert client.post("/", data={"url": "https://example.com/video"}).status_code == 502

def test_timeout():
    import subprocess
    with patch("app.subprocess.run", side_effect=subprocess.TimeoutExpired("yt-dlp", 180)):
        assert client.post("/", data={"url": "https://example.com/video"}).status_code == 504

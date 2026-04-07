from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import subprocess
import tempfile
import os
import html

app = FastAPI()

HTML = """<html>
<head>
<meta charset="utf-8">
<title>FeliuS Transcriber</title>
</head>
<body style="font-family:Arial,sans-serif;max-width:900px;margin:40px auto;">
<h2>FeliuS Transcriber</h2>
<form method="post">
<input name="url" style="width:700px;padding:8px;" placeholder="Pegá URL de TikTok"/>
<button type="submit" style="padding:8px 12px;">Transcribir</button>
</form>
<pre style="white-space:pre-wrap;background:#f5f5f5;padding:16px;border-radius:8px;">{}</pre>
</body>
</html>"""

@app.get("/", response_class=HTMLResponse)
def home():
    return HTML.format("")

@app.post("/", response_class=HTMLResponse)
def transcribe(url: str = Form(...)):
    try:
        with tempfile.TemporaryDirectory() as tmp:
            audio_base = os.path.join(tmp, "audio")

            subprocess.run([
                "yt-dlp",
                "-x",
                "--audio-format", "mp3",
                "-o", audio_base + ".%(ext)s",
                url
            ], check=True, capture_output=True, text=True)

            audio_path = audio_base + ".mp3"

            env = os.environ.copy()
            env["CUDA_VISIBLE_DEVICES"] = ""

            result = subprocess.run(
                [
                    "whisper", audio_path,
                    "--model", "base",
                    "--device", "cpu",
                    "--language", "es",
                    "--fp16", "False"
                ],
                capture_output=True,
                text=True,
                check=True,
                env=env
            )

            salida = result.stdout.strip() or "Sin transcripción"
            return HTML.format(html.escape(salida))

    except subprocess.CalledProcessError as e:
        err = (e.stdout or "") + "\n" + (e.stderr or "")
        return HTML.format(html.escape(err.strip() or str(e)))

    except Exception as e:
        return HTML.format(html.escape(str(e)))


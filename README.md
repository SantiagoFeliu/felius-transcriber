# Felius Transcriber

**Local video-to-text workflow — Python, FastAPI, yt-dlp and OpenAI Whisper.**

Felius Transcriber is a small web application for extracting speech from online videos and reviewing the resulting text. It was built to make short technical videos easier to study, compare and assess without sending audio to a hosted transcription API.

> **Status:** Local utility. The current implementation is Spanish-language, CPU-based and intended for trusted local use.

## What it does

1. Accepts a video URL through a simple browser form.
2. Uses `yt-dlp` to extract audio as MP3.
3. Runs the `whisper` command locally using the `base` model, CPU execution and Spanish language settings.
4. Displays the transcription command's console output in the browser.

The downloaded audio is stored in a temporary directory that is cleaned up after processing. The current web application **does not provide a dedicated transcript download or subtitle export interface**.

## Architecture

```mermaid
flowchart LR
    A[Browser form] --> B[FastAPI]
    B --> C[yt-dlp audio extraction]
    C --> D[Temporary MP3]
    D --> E[Local Whisper CLI on CPU]
    E --> F[Browser result]
```

## Technology

- Python and FastAPI — local web application
- yt-dlp — media retrieval and audio extraction
- ffmpeg — audio conversion dependency
- OpenAI Whisper CLI — local speech transcription
- Uvicorn — application server

## Requirements

- Python 3
- `ffmpeg` installed and available on `PATH`
- Access to download the source video, subject to the platform's rules and permissions
- Enough local resources for Whisper's `base` model

The supplied `requirements.txt` includes pinned Python dependencies, including PyTorch and CUDA-related packages. Installation size and compatibility can vary by platform; **CPU transcription is explicitly selected in the application code**.

## Installation

```bash
git clone https://github.com/SantiagoFeliu/felius-transcriber.git
cd felius-transcriber
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Confirm that `ffmpeg`, `yt-dlp` and `whisper` are available before running the app.

## Run locally

```bash
uvicorn app:app --host 127.0.0.1 --port 8000
```

Open **http://127.0.0.1:8000** in your browser, paste a supported video URL and submit the form.

The implementation currently calls Whisper with these fixed options:

```text
--model base --device cpu --language es --fp16 False
```

The model may need to be downloaded on first use.

## Current limitations

- The web form and processing settings are designed for Spanish transcription.
- There is no authentication, URL allowlist, request queue or rate limiting; **do not expose the service publicly**.
- The request runs external processes synchronously, so processing may take time.
- Video downloads depend on source availability, site restrictions and `yt-dlp` support.
- The app displays command output and error details in the browser. Do not submit sensitive URLs or content.
- No automated test suite or production deployment guarantees are demonstrated.
- Although Whisper may create auxiliary output files, the current application does not expose them through its interface.

## Why it exists

Technical information is often shared in short videos rather than searchable documentation. This utility provides a local workflow for turning spoken material into text that can be inspected and compared.

**Scope:** A practical, source-available local implementation—not a hosted transcription service or a production-ready media processing platform.

# FeliuS Transcriber

Transcriptor local de videos de TikTok.

## Qué hace
Pegás una URL, descarga el audio, lo transcribe localmente y muestra el texto en el navegador.

## Stack
- FastAPI
- Uvicorn
- yt-dlp
- openai-whisper
- python-multipart

## Requisitos
- Python 3
- ffmpeg

## Instalación
git clone https://github.com/SantiagoFeliu/felius-transcriber.git
cd felius-transcriber

python3 -m venv venv
source venv/bin/activate

pip install fastapi uvicorn yt-dlp openai-whisper python-multipart

## Ejecutar
uvicorn app:app --reload

Abrir:
http://127.0.0.1:8000

## Seguridad
- Todo corre localmente
- No usa APIs externas
- No incluye credenciales ni archivos sensibles

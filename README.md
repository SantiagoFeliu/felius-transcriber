# Felius Transcriber

Transcribe videos de TikTok o cualquier video a texto localmente para analizarlos, estudiar herramientas y evaluar contenido técnico sin depender de APIs externas.

## Qué resuelve

Convierte contenido rápido en texto utilizable para decidir si una herramienta, repo o idea realmente vale la pena.

## Uso real

Este proyecto sirve para:

- analizar videos técnicos de TikTok
- extraer información útil de contenido corto
- revisar herramientas, repositorios y conceptos
- convertir video en texto para estudio y evaluación

## Cómo funciona

1. ingresás una URL de TikTok
2. se descarga el audio
3. se transcribe localmente
4. obtenés el texto para analizar

## Stack

- FastAPI
- yt-dlp
- Whisper
- Python

## Requisitos

- Python 3
- ffmpeg

## Instalación

git clone https://github.com/SantiagoFeliu/felius-transcriber.git
cd felius-transcriber
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

## Ejecutar

uvicorn app:app --reload

Abrir en navegador:
http://127.0.0.1:8000

## Output

- transcripción en texto
- subtítulos y archivos derivados según el proceso

## Por qué existe

Permite transformar contenido corto en información analizable para decidir rápido si algo sirve o no.

## Estado

Uso diario para análisis de contenido técnico.

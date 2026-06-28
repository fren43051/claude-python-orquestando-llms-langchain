# 2199 — Python y Claude: Orquestando LLMs con LangChain

## Resumen

Proyecto demo en Python que muestra cómo orquestar modelos de lenguaje para el análisis y la generación de resúmenes sobre imágenes. El flujo combina un modelo para análisis objetivo (Claude) y otro para generar un resumen claro para usuarios (Cohere), usando LangChain como framework de orquestación.

## Características

- Codificación de imágenes a base64 para inclusión en prompts.
- Prompt estructurado para análisis objetivo de imágenes.
- Composición de cadenas (chains) con LangChain para análisis + resumen.
- Configuración mediante variables de entorno (.env).

## Estructura principal

- `lang_chain.py` — Script principal que arma prompts, llama a los LLMs y muestra resultados.
- `my_helper.py` — Funciones utilitarias (ej. `encode_image`).
- `my_keys.py` — Lectura de variables de entorno y nombres de modelo.
- `my_models.py` — Constantes con nombres de modelos.
- `datos/` — Carpeta para imágenes de ejemplo (ej. `ejemplo_grafico.jpg`).
- `requirements.txt` — Dependencias del proyecto.

## Requisitos

- Python 3.8+ (recomendado 3.10+)
- Cuentas y API keys para los proveedores usados (Claude, Cohere, etc.)
- Conexión a Internet para llamadas a API

## Instalación rápida

1. Clona el repositorio:
```bash
git clone https://github.com/fren43051/claude-python-orquestando-llms-langchain.git
cd claude-python-orquestando-llms-langchain/2199-python-y-claude-orquestando-llms-con-langchain
```

2. Crear y activar un entorno virtual:
- Windows:
```bash
python -m venv .venv-claude-3
.\.venv-claude-3\Scripts\activate
```
- macOS / Linux:
```bash
python3 -m venv .venv-claude-3
source .venv-claude-3/bin/activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Configuración de claves (archivo .env)

Crea un archivo `.env` en la carpeta del proyecto con las siguientes variables (ejemplo):
```
GEMINI_API_KEY=TU_GEMINI_API_KEY
COHERE_API_KEY=TU_COHERE_API_KEY
COHERE_MODEL_NAME=command-r-plus-08-2024
CLAUDE_API_KEY=TU_CLAUDE_API_KEY
CLAUDE_MODEL_NAME=claude-sonnet-4-6
```

## Uso

1. Coloca una imagen de prueba en `datos/ejemplo_grafico.jpg` (o ajusta la ruta en `lang_chain.py`).
2. Ejecuta:
```bash
python lang_chain.py
```

Salida esperada:
- Un bloque con la respuesta analítica generada por Claude (descripción + etiquetas).
- Un resumen final generado por Cohere en lenguaje claro y orientado al público objetivo.

## Dependencias principales

Revisar `requirements.txt`. Ejemplos clave:
- langchain
- langchain-cohere
- langchain-anthropic (o adaptador equivalente)
- pillow
- python-dotenv
- httpx, pydantic

## Puntos de atención y troubleshooting

- Asegúrate de que los nombres de modelo (`CLAUDE_MODEL_NAME`, `COHERE_MODEL_NAME`) sean compatibles con tus cuentas y versiones de adaptadores.
- Si las llamadas a la API fallan, revisa las variables de entorno y los límites de cuota del proveedor.
- El proyecto usa encodificación base64 para imágenes — verifica que el archivo no esté corrupto y que la ruta sea correcta.
- Versiones de LangChain: la API interna puede cambiar entre versiones; si encuentras errores de invocación, revisa la versión instalada frente a `requirements.txt`.

## Extensiones recomendadas

- Convertir el script en una CLI para procesar carpetas completas y generar JSON con resultados.
- Guardar resultados en un archivo (CSV/JSON) para análisis posterior.
- Añadir evaluación automática con ejemplos anotados para medir consistencia del análisis.

## Contribuciones

import sys
import io

# Configurar la salida estándar para manejar UTF-8 en Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from langchain_anthropic import ChatAnthropic
# from langchain_openai import ChatOpenAI
from my_keys import CLAUDE_API_KEY, CLAUDE_MODEL_NAME  # , QWEN_API_KEY, QWEN_MODEL_NAME
from my_helper import encode_image
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.globals import set_debug
from detalles_imagen import DetallesImagen

set_debug(True)

# Modelos
claude_model = CLAUDE_MODEL_NAME or "claude-sonnet-4-6"
# qwen_model = QWEN_MODEL_NAME or "qwen3.7-plus"

# Clientes LLM
llm_claude = ChatAnthropic(
    api_key=CLAUDE_API_KEY,
    model_name=claude_model
)

# llm_qwen = ChatOpenAI(
#     api_key=QWEN_API_KEY,
#     model=qwen_model,
#     base_url="https://ws-6ddr8e0xpui1by88.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1",
#     temperature=0.3
# )

# Imagen
imagen = encode_image('datos/ejemplo_grafico.jpg')

# Template de análisis (Claude)
template_analisis = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
Asume que eres analista de imágenes. Tu principal tarea consiste en: analizar una imagen 
para extraer las informaciones más relevantes de manera objetiva.

# FORMATO DE SALIDA
Descripción de la imagen: Tu descripción de la imagen aquí.
Etiquetas: Una lista con 3 palabras-clave separadas con comas.
"""
        ),
        (
            "user",
            [
                {
                    "type": "text",
                    "text": "Describe la imagen: "
                },
                {
                    "type": "image_url",
                    "image_url": "data:image/jpeg;base64,{imagen_informada}"
                }
            ]
        )
    ]
)

parser_json = JsonOutputParser(
    pydantic_object=DetallesImagen
)

# Template de resumen (Qwen)
template_respuesta = PromptTemplate(
    template="""
Genera un resumen, utilizando un lenguaje claro y objetivo, enfocado en el público colombiano.
La idea es que la comunicación del resultado sea lo más sencilla posible, priorizando los registros
para consultas posteriores.

#RESULTADO DE LA IMAGEN
{respuesta_analisis_imagen}

#FORMATO DE SALIDA
{formato_salida}
""",
    input_variables=["respuesta_analisis_imagen"],
    partial_variables={
        "formato_salida": parser_json.get_format_instructions()
    }
)

# Cadenas
cadena_analisis = template_analisis | llm_claude | StrOutputParser()
cadena_resumen = template_respuesta | llm_claude | parser_json
cadena_compuesta = (cadena_analisis | cadena_resumen)

# Ejecución
respuesta = cadena_compuesta.invoke({"imagen_informada": imagen})
print(respuesta)

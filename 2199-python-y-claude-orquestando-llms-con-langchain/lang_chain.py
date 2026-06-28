import sys
import io

# Configurar la salida estándar para manejar UTF-8 en Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from langchain_anthropic import ChatAnthropic
from langchain_cohere import ChatCohere
from langchain_core.messages import HumanMessage
from my_keys import CLAUDE_API_KEY, CLAUDE_MODEL_NAME, COHERE_API_KEY, COHERE_MODEL_NAME
from my_helper import encode_image
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.globals import set_debug

set_debug(True)

# Fallback to a currently supported model if the env variable is missing
# or points to a deprecated snapshot.
claude_model = CLAUDE_MODEL_NAME or "claude-sonnet-4-6"
cohere_model = COHERE_MODEL_NAME or "command-r-plus-08-2024"

llm_claude = ChatAnthropic(
    api_key=CLAUDE_API_KEY,
    model_name=claude_model
)


imagen = encode_image('datos/ejemplo_grafico.jpg')
pregunta = "Describe la imagen"

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

cadena_analisis = template_analisis | llm_claude | StrOutputParser()

respuesta_analisis = cadena_analisis.invoke({"imagen_informada": imagen})

print(respuesta_analisis)

template_respuesta = PromptTemplate(
    template="""
Genera un resumen, utilizando un lenguaje claro y objetivo, enfocado en el público colombiano.
La idea es que la comunicación del resultado sea lo más sencilla posible, priorizando los registros
para consultas posteriores.

#RESULTADO DE LA IMAGEN
{respuesta_analisis_imagen}
""",
    input_variables=["respuesta_analisis_imagen"]
)

llm_cohere = ChatCohere(cohere_api_key=COHERE_API_KEY
)
cadena_resumen = template_respuesta | llm_cohere | StrOutputParser()

cadena_compuesta = (cadena_analisis | cadena_resumen)

respuesta = cadena_compuesta.invoke({"imagen_informada": imagen})
print(respuesta)
from langchain.tools import BaseTool
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from my_keys import QWEN_API_KEY, QWEN_MODEL_NAME
import ast

class HerramientaExplicar(BaseTool):
    name: str = "HerramientaExplicar"
    description: str = """
                            Utiliza esta herramienta siempre que sea solicitada la explicación de un contenido a las personas.

                            # ENTRADA REQUERIDA
                            - 'tema' (str): Tema principal informado en la pregunta del usuario. 
                              Ejemplo: test.jpg o test.jpeg
                            """
    return_direct: bool = True

    def _run(self, accion):
        accion = ast.literal_eval(accion)
        tema_parametro = accion.get("tema", "")

        llm_qwen = ChatOpenAI(
            api_key=QWEN_API_KEY,
            model=QWEN_MODEL_NAME,
            base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
            temperature=0.0
        )

        template_respuesta = PromptTemplate(
                                template =  """
                                            Asume el papel de un profesor con aspectos de didatica del usuario.
                                            1. Elabora una explicacion sobre el tema {tema} que sea de facil 
                                            comprension para estudiantes de secuandaria.
                                            2. Utiliza ejemplos cotidianos para volver la explicacion mas sencilla.
                                            3. En caso de que surja algun recurso para apoyar la explicacion, recuerda el escenario del contexto colombiano.
                                            4. En caso presentes algun script de codigo, se didactico y usa python.
                                            
                                            tema pregunta: {tema}
                                            """,
                            input_variables=["tema"]
                        )

        cadena = template_respuesta | llm_qwen | StrOutputParser()

        respuesta = cadena.invoke({"tema": tema_parametro})

        return respuesta
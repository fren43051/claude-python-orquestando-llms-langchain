from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from my_models import CLAUDE_SONNET, QWEN_37_PLUS
from my_keys import CLAUDE_API_KEY, QWEN_API_KEY
from langchain_core.globals import set_debug
from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import Tool
from herramienta_analisis_imagen import HerramientaAnalisisImagen

set_debug(False)

class AgenteOrquestador:
    def __init__(self):
        self.llm = ChatAnthropic(
            api_key=CLAUDE_API_KEY,
            model_name=CLAUDE_SONNET
        )

        herramienta_analisis_imagen = HerramientaAnalisisImagen()

        self.tools = [
            Tool(
                name=herramienta_analisis_imagen.name,
                func=herramienta_analisis_imagen.run,
                description=herramienta_analisis_imagen.description,
                return_direct=herramienta_analisis_imagen.return_direct
            )
        ]

        prompt = hub.pull("hwchase17/react")

        self.agent = create_react_agent(self.llm, self.tools, prompt)

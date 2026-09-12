import os
from anthropic import Anthropic
from dotenv import load_dotenv
from .tools import TOOLS_SCHEMA, run_tool

load_dotenv()

agent_instructions = "O agente é responsável por responder perguntas de um banco de dados, inicialmente utilizando a função get_info_tabelas caso não saiba as tabelas do banco e seus atributos. Sempre utilizando a função run_sql_query quando que precisar de um dado real do banco, sem inventar valores. Sempre responder em português brasileiro."


def perguntar(pergunta_usuario: str):
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    messages = [{"role": "user", "content": pergunta_usuario}]

    while True:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            system=agent_instructions,
            tools=TOOLS_SCHEMA,
            messages=messages
        )

        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "tool_use":
            results_list = []
            for block in response.content:
                if block.type == "tool_use":
                    result = run_tool(block.name, block.input)
                    results_list.append({"type": "tool_result", "tool_use_id": block.id, "content": str(result)})
            messages.append({"role": "user", "content": results_list})
        elif response.stop_reason == "end_turn":
            answer = ""
            for block in response.content:
                if block.type == "text":
                    answer += block.text
            return answer
        else:
            return "Não consegui gerar uma resposta completa. Tente reformular a pergunta."
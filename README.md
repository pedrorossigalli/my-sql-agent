# My SQL Agent

Converte texto em linguagem natural para consultas à um Banco de Dados de forma simples e segura.

## Sobre o projeto

O projeto foi feito para colocar em prática conceitos de agentes e de SQL, de modo a ajudar pessoas não familiarizadas com linguagens de programação a extrair informações de bancos de dados usando perguntas em linguagem natural. Conceitos de function calling e segurança na linguagem SQL foram praticados durante o processo de desenvolvimento do My SQL Agent.

## Status

Em desenvolvimento.

## Como rodar (por enquanto)

1. Crie um ambiente virtual e instale as dependências:
    bash
    python -m venv venv
    pip install -r requirements.txt

2. Crie o BD:
    bash
    python -m src.database


## Decisões técnicas

- O preço foi separado em snapshots na pesagem, para que a alteração futura do preço do material não influencie em pesagens passadas
- FOREIGN KEY com PRAGMA ativado para que não se adicione clientes ou materiais inexistentes
- O programa utiliza os dados em CSV para alimentar o BD
- database.py só pode ser rodado uma vez, o que impede inserir o mesmo dado novamente no BD
- CSVs com dados inseridos no repositório com o objetivo de facilitar testes
- Segurança via Regex para que as queries no banco de dados não contenham outra consulta a não ser SELECT

## Próximos passos

- Criar main.py para que o usuario possa fazer varias perguntas ao modelo
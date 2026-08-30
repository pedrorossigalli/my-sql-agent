# My SQL Agent

Converte texto em linguagem natural para consultas à um Banco de Dados de forma simples e segura.

## Sobre o projeto

O projeto foi feito para colocar em prática conceitos de agentes e de SQL, de modo a ajudar pessoas não familiarizadas com linguagens de programação a extrair informações de bancos de dados usando perguntas em linguagem natural. Conceitos de function calling e segurança na linguagem SQL foram praticados durante o processo de desenvolvimento do My SQL Agent.

## Status

🔧 Em desenvolvimento.

## Arquitetura

my-sql-agent/
├── data/ # banco de dados SQLite (gerado localmente)
└── src/
└── database.py # cria as tabelas: Materiais, Clientes, Pesagens

## Como rodar (por enquanto)

1. Crie um ambiente virtual e instale as dependências:
    bash
    python -m venv venv
    pip install -r requirements.txt

2. Crie o banco de dados:
    bash
    python -m src.database


## Decisões técnicas

- O preço foi separado em snapshots na pesagem, para que a alteração futura do preço do material não influencie em pesagens passadas
- FOREIGN KEY com PRAGMA ativado para que não se adicione clientes ou materiais inexistentes

## Próximos passos

- Preencher o banco de dados com os materiais (Pó de pedra, Pedra britada 01, Pedra britada 02, Rachão, Calcário) e dados fictícios de clientes e pesagens
- Implementar a API da Claude via function calling
- Adicionar validação de segurança nas queries geradas pelo modelo
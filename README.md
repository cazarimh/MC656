# Projeto de Organização Financeira (MC656)

O projeto consiste no desenvolvimento de um sistema digital voltado para auxiliar indivíduos no gerenciamento de suas finanças pessoais. A aplicação permitirá que o usuário cadastre seus gastos mensais, visualize a distribuição de despesas por meio de gráficos interativos e acompanhe a evolução de seu orçamento ao longo do tempo. Dessa forma, busca-se promover a educação financeira, incentivar o consumo consciente e contribuir para os Objetivos de Desenvolvimento Sustentável (ODS) 4 — Educação de Qualidade e ODS 8 — Trabalho Decente e Crescimento Econômico.

## Como Rodar o Projeto Localmente

### Pré-requisitos

- **Node.js:** Versão 22.18.0
- **Python:** Versão 3.13.7

### Backend

1. Navegue até a pasta do backend: `cd backend`
2. Crie e ative um ambiente virtual: `python -m venv venv` e `source venv/Scripts/activate`
3. Instale as dependências: `pip install -r requirements.txt`
4. Rode o servidor: `uvicorn main:app --reload`

### Frontend

1. Navegue até a pasta do frontend: `cd frontend`
2. Instale as dependências: `npm install`
3. Rode o servidor de desenvolvimento: `npm run dev`

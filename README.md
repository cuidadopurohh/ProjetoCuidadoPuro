# Projeto Cuidado Puro

Este repositório contém o backend FastAPI e um placeholder de frontend estático.

## Deploy no Render

### Backend
1. Conecte este repositório no Render.
2. Crie um serviço do tipo **Web Service**.
3. Defina:
   - `Root Directory`: `/`
   - `Environment`: `Python`
   - `Build Command`: `pip install -r requirements.txt`
   - `Start Command`: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Adicione a variável de ambiente no Render:
   - `DATABASE_URL`
   - valor: `postgresql://neondb_owner:npg_bIga8HieqFn7@ep-dawn-truth-acuzigkq.sa-east-1.aws.neon.tech/neondb?sslmode=require`

### Frontend
1. Crie um serviço do tipo **Static Site**.
2. Defina:
   - `Root Directory`: `/`
   - `Publish Directory`: `static`

## Banco de dados Neon

O backend já está preparado para ler `DATABASE_URL` do ambiente. Em Render, configure essa variável de ambiente como segredo.

## Observações

- A pasta `venv/` não deve ser enviada para o repo; ela está no `.gitignore`.
- O `static/` atual é um placeholder e pode ser substituído pelo seu código real.

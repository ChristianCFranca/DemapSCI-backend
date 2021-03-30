# Utilizado para debugging facilitar o deploy
import uvicorn

# Acessar variáveis de ambiente
import os

# Obtém as rotas disponíveis na API
from routers.ar_condicionado.fancoils import fancoils
from routers.energia.subestacoes import subestacoes

# Importa a classe FastAPI para criar o APP
from fastapi import FastAPI

# Lidar com CORS
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="DEMAP-SCI", description="REST API para realizar cadastro de infraestrutura do Demap do Banco Central.", version="0.1.0")

# Inclui as rotas disponíveis
app.include_router(fancoils.router)
app.include_router(subestacoes.router)

origins = [
    "*" # Todos permitidos
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["home"], summary="Home Page")
async def home():
    return {"message": "Hello DEMAP-SCI!"}

if __name__ == "__main__":
    port = os.environ.get('PORT') if os.environ.get('PORT') else 80 # Para deploy no Heroku
    uvicorn.run(app, host="0.0.0.0", port=port)
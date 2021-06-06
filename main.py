# Acessar variáveis de ambiente
import os

if os.path.exists(".env"): # Carrega as variaveis de ambiente de desenvolvimento
    from dotenv import load_dotenv
    load_dotenv()

if os.path.exists("./packages"): # Para deploy no AWS Lambda
    import sys
    sys.path.insert(0, "./packages")

# Obtém as rotas disponíveis na API
import auth
from routers.ar_condicionado import crud_api

# Importa a classe FastAPI para criar o APP
from fastapi import FastAPI

# Lidar com CORS
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="DEMAP-SCI", description="REST API para realizar cadastro de infraestrutura do Demap do Banco Central.", version="0.2.0")

# Inclui as rotas disponíveis
app.include_router(crud_api.router)
app.include_router(auth.router)

origins = [
    "http://localhost:8080",
    "https://demap-sci-frontend.herokuapp.com",
    "https://demapsci.herokuapp.com"
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
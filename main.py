# Acessar variáveis de ambiente
import os

if os.path.exists(".env"): # Carrega as variaveis de ambiente de desenvolvimento
    from dotenv import load_dotenv
    load_dotenv()

AWS_LAMBDA_ENV = os.environ.get('AWS_LAMBDA_ENV')

if not AWS_LAMBDA_ENV:
    print("\033[94mAWS_LAMBDA:\033[0m" + "\t  No AWS_LAMBDA_ENV env available. Loading as False...")
    AWS_LAMBDA_ENV = False
else:
    if AWS_LAMBDA_ENV == "true":
        AWS_LAMBDA_ENV = True
    else:
        AWS_LAMBDA_ENV = False

if not os.path.exists("./packages") and AWS_LAMBDA_ENV:
    print("\033[93mAWS_LAMBDA:\033[0m" + "\t  If AWS_LAMBDA_ENV is set, the \'packages\' folder must be provided. Setting AWS_LAMBDA_ENV to False...")
    AWS_LAMBDA_ENV = False

if AWS_LAMBDA_ENV:
    import sys
    sys.path.insert(0, "./packages")

# Obtém as rotas disponíveis na API
import auth
from app_crud import app_crud

# Importa a classe FastAPI para criar o APP
from fastapi import FastAPI

# Lidar com CORS
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="DEMAP-SCI", description="REST API para realizar cadastro de infraestrutura do Demap do Banco Central.", version="0.2.0")

# Inclui as rotas disponíveis
app.include_router(app_crud.router)
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

if AWS_LAMBDA_ENV: # Para deploy no AWS Lambda
    from mangum import Mangum
    handler = Mangum(app)
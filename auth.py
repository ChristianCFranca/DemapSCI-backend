from fastapi import Depends, HTTPException, APIRouter, status

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional

from datetime import datetime, timedelta # Lidar com a relação de tempo do JWT

from jose import JWTError, jwt

import os

SCI_USERNAME = os.environ.get("SCI_USERNAME")
if not SCI_USERNAME:
    print("\033[93mUSERNAME:\033[0m\t No SCI_USERNAME env available.")
    SCI_USERNAME = "admin"

SCI_PASSWORD = os.environ.get("SCI_PASSWORD")
if not SCI_PASSWORD:
    print("\033[93mPASSWORD:\033[0m\t No SCI_PASSWORD env available.")
    SCI_PASSWORD = "admin"

# Define nosso router
router = APIRouter(prefix="/auth", tags=["Autenticação"])

SECRET_KEY = os.environ.get("SECRET_KEY") # Não deve estar exposto em código
if not SECRET_KEY:
    raise Exception("No SECRET_KEY available...")
else:
    print("\033[94m"+"AUTH:" + "\033[0m" + "\t  SECRET KEY environment data available! Loaded.")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")
if not ACCESS_TOKEN_EXPIRE_MINUTES:
    print("\033[93m" + "AUTH:" + "\033[0m" + "\t  No ACCESS_TOKEN_EXPIRE_MINUTES available...")
    ACCESS_TOKEN_EXPIRE_MINUTES = 10 # Padrão de 10 minutos para desenvolvimento
else:
    try:
        ACCESS_TOKEN_EXPIRE_MINUTES = int(ACCESS_TOKEN_EXPIRE_MINUTES)
        print("\033[94m"+"AUTH:" + "\033[0m" + "\t  EXPIRE TIME environment data available! Loaded.")
    except:
        print("\033[94m"+"AUTH:" + "\033[0m" + "\t  EXPIRE TIME environment data was found but could not be casted to an int. Loading base 5 minutes expire.")
        ACCESS_TOKEN_EXPIRE_MINUTES = 5 # Padrão de 5 minutos para desenvolvimento

# Modelos -------------------------------
class User(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
# ---------------------------------------

# Define o esquema OAuth2 para autenticacao
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# Cria o token de acesso
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy() # Copia o dicionário em um novo
    if expires_delta:
        expire = datetime.utcnow() + expires_delta # Se houve tempo de expiração, o expire recebe o horário atual + o horário da diferença (logo, agora + 30 minutos)
    else:
        expire = datetime.utcnow() + timedelta(minutes=5) # Se não, utiliza o padrão (agora + 5 minutos)
    to_encode.update({"exp": expire}) # Atualiza o dicionario to_encode com a informação de expiração
    encoded_jwt = jwt.encode( # Podemos agora criar a string JWT
        to_encode, # Passamos o dicionario que esta no formato {"sub": username, "expire": horario_de_agora}
        SECRET_KEY, # Passamos a secret key para a assinatura. NÃO DEVE SER COMPARTILHADA COM NADA NEM NINGUÉM
        algorithm=ALGORITHM # O algoritmo é o HS256 (só a aplicação do servidor terá controle sobre quem usa, não é necessário RS256, outro motivo pra manter a SECRET_KEY muito bem guardada)
        )
    return encoded_jwt # Retorna a string XXXX.XXXX.XXXX

# Obtemos o usuário atual. Essa é a função que cuida de verificar se o usuário que está logado ainda não expirou
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try: # O bloco try existe pois o jwt.decode gera uma exceção JWTError se a assinatura tiver sido inválida. Se ocorrer outra coisa fora o JWT o programa é derrubado
        payload = jwt.decode( # Decodifica o JWT, ficando atento à data de expiração
            token, # Utiliza o token string
            SECRET_KEY, # Utiliza a SECRET_KEY
            algorithms=[ALGORITHM] # Utiliza o mesmo algoritmo utilizado na codificação
            )
        username: str = payload.get("sub") # Obtém o usuário interno "subject" do JWT
        if username is None or username != SCI_USERNAME: # Verifica se ele não foi None (key não existe no dicionario)
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return

async def valid_user(token: str = Depends(oauth2_scheme)): # Função que retorna outra função. Útil para utilizar o Depends do fastapi
    await get_current_user(token)
    return

# A autenticação começa aqui. Se tudo der certo, a resposta é do modelo {"token": SEU_TOKEN, "token_type": "bearer"}
@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()): # Utiliza a dependencia OAuth2PasswordRequestForm, que captura as informacoes no padrao OAuth2 (form-data, etc)
    if form_data.username != SCI_USERNAME or form_data.password != SCI_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, # Status code de não autorizado
            detail="Nome de usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)  # Representa a diferença entre dois objetos datetime. Aqui a configuração está em minutos
    access_token = create_access_token( # Cria o token de acesso pro usuário que acabou de realizar login
        data={"sub": SCI_USERNAME},  # Passa o usuario (sempre é possível obtê-lo do JWT depois), mas pode ser absolutamente qualquer informacao
        expires_delta=access_token_expires # Passamos o tempo de expiração
    )
    return Token(**{"access_token": access_token, "token_type": "bearer"}) # Isso é salvo pela aplicação, que pode usar como bem entender

@router.get("/me", dependencies=[Depends(get_current_user)])
async def get_me():
    return {"detail": "OK"}
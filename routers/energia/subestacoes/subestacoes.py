# Importa a classe de rotas do FastAPI e todas as dependências úteis dela
from fastapi import Depends, FastAPI, HTTPException, APIRouter
from typing import List

# SQLAlchemy
from sqlalchemy.orm import Session

# Importa as tabelas em SQL e os esquemas esperados
from . import models, schemas

# Importa funcionalidades do CRUD
from CRUD import crud
from CRUD.crud import get_db

# Também importa a Engine e a utiliza para criar as tabelas
from database import engine
models.Base.metadata.create_all(bind=engine)

# ----------------------------------------------------------------------------------------

# Define nosso router
router = APIRouter(prefix="/energia/subestacoes", tags=["Subestações"])

# Rotas ----------------------------------------------------------------------------------
@router.get("/", summary="Obtém todos as subestações", response_model=List[schemas.SubestacaoResponse])
def get_subestacoes(db: Session = Depends(get_db)):
    db_item = crud.get_items(db, model=models.Subestacao)
    return db_item

@router.get("/tags", summary="Obtém todos as tags de todas as subestações", response_model=List[str])
def get_all_subestacoes_tags(db: Session = Depends(get_db)):
    db_item = crud.get_all_tags(db, model=models.Subestacao)
    db_item = [item["tag"] for item in db_item]
    return db_item

@router.get("/{subest_id}", response_model=schemas.SubestacaoResponse)
def get_subestacao(subest_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_by_id(db, model=models.Subestacao, item_id=subest_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Subestação não encontrada")
    return db_item

@router.post("/", summary="Cadastra uma nova subestação", response_model=schemas.SubestacaoResponse)
def post_subestacao(fancoil: schemas.SubestacaoRequest, db: Session = Depends(get_db)):
    db_item = crud.get_by_tag(db, model=models.Subestacao, item_tag=fancoil.tag)
    if db_item:
        raise HTTPException(status_code=400, detail="Subestação já registrado")
    return crud.create_item(db=db, model=models.Subestacao, item=fancoil)

@router.put("/{subest_id}", summary="Altera uma subestação existente")
def put_subestacao(subest_id: int, fancoil: schemas.SubestacaoRequest, db: Session = Depends(get_db)):
    db_item = crud.get_by_id(db, model=models.Subestacao, item_id=subest_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Subestação não encontrada")
    db_item = crud.get_by_tag(db, model=models.Subestacao, item_tag=fancoil.tag)
    if db_item is not None:
        if db_item.id != subest_id:
            raise HTTPException(status_code=400, detail="Subestações não podem compartilhar uma mesma tag")

    return crud.update_item(db, model=models.Subestacao, item_id=subest_id, item=fancoil)

@router.delete("/{subest_id}", summary="Deleta uma subestação existente")
def delete_subestacao(subest_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_by_id(db, model=models.Subestacao, item_id=subest_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Subestação não encontrada")
    return crud.delete_item(db, model=models.Subestacao, item_id=subest_id)
# ----------------------------------------------------------------------------------------
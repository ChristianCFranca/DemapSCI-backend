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
router = APIRouter(prefix="/ar-condicionado/fancoils", tags=["equipamentos"])

# Rotas ----------------------------------------------------------------------------------
@router.get("/", summary="Obtém todos os fancoils", response_model=List[schemas.FanCoilResponse])
def get_fancoils(db: Session = Depends(get_db)):
    db_item = crud.get_items(db, model=models.FanCoil)
    return db_item

@router.get("/tags", summary="Obtém todos as tags de todas os fancoils", response_model=List[str])
def get_all_fancoils_tags(db: Session = Depends(get_db)):
    db_item = crud.get_all_tags(db, model=models.FanCoil)
    db_item = [item["tag"] for item in db_item]
    return db_item

@router.get("/{fancoil_id}", response_model=schemas.FanCoilResponse)
def get_fancoil(fancoil_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_by_id(db, model=models.FanCoil, item_id=fancoil_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Fancoil não encontrado")
    return db_item

@router.post("/", summary="Cadastra um novo fancoil", response_model=schemas.FanCoilResponse)
def post_fancoil(fancoil: schemas.FanCoilRequest, db: Session = Depends(get_db)):
    db_item = crud.get_by_tag(db, model=models.FanCoil, item_tag=fancoil.tag)
    if db_item:
        raise HTTPException(status_code=400, detail="Fancoil já registrado")
    return crud.create_item(db=db, model=models.FanCoil, item=fancoil)

@router.put("/{fancoil_id}", summary="Altera um fancoil existente")
def put_fancoil(fancoil_id: int, fancoil: schemas.FanCoilRequest, db: Session = Depends(get_db)):
    db_item = crud.get_by_id(db, model=models.FanCoil, item_id=fancoil_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Fancoil não encontrado")
    db_item = crud.get_by_tag(db, model=models.FanCoil, item_tag=fancoil.tag)
    if db_item is not None:
        if db_item.id != fancoil_id:
            raise HTTPException(status_code=400, detail="Fancoils não podem compartilhar uma mesma tag")

    return crud.update_item(db, model=models.FanCoil, item_id=fancoil_id, item=fancoil)

@router.delete("/{fancoil_id}", summary="Deleta um fancoil existente")
def delete_fancoil(fancoil_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_by_id(db, model=models.FanCoil, item_id=fancoil_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Fancoil não encontrado")
    return crud.delete_item(db, model=models.FanCoil, item_id=fancoil_id)
# ----------------------------------------------------------------------------------------
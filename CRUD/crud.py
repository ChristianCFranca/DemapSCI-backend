from sqlalchemy.orm import Session

# Importa as dependências
from database import Base, SessionLocal

# Dependencia do db
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Funções de CRUD -------------------------------------------------------------------
def get_items(db: Session, model):
    return db.query(model).all()

def get_all_tags(db: Session, model):
    return db.query(model.tag).all()

def get_by_id(db: Session, model, item_id: int):
    return db.query(model).filter(model.id == item_id).first()

def get_by_tag(db: Session, model, item_tag: str):
    return db.query(model).filter(model.tag == item_tag).first()

def create_item(db: Session, model, item):
    db_item = model(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_item(db: Session, model, item_id: int, item):
    db_item = db.query(model).filter(model.id == item_id).update(item.dict(), synchronize_session="fetch")
    db.commit()
    return db_item

def delete_item(db: Session, model, item_id: int):
    db_item = db.query(model).filter(model.id == item_id).delete(synchronize_session="fetch")
    db.commit()
    return db_item
# ----------------------------------------------------------------------------------------
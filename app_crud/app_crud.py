
# Importa a classe de rotas do FastAPI e todas as dependências úteis dela
from fastapi import Depends, Query, HTTPException, status
from utils.APIRouter import APIRouter
from fastapi.responses import StreamingResponse
from auth import valid_user

# Pegar o json da Query
import urllib
import json

# Importa os typings para definir tipos de resposta esperados
from typing import Optional, List

# Importa o crud_handler para a coleção atual
from database import crud_handler

# Para baixar como .csv
import pandas as pd
from datetime import date
from io import StringIO

# Controlador de Schemas
from equipments.EquipmentsTypeController import EquipmentsTypeController

# Dependências ---------------------------------------------------------------------------
schema_controller = EquipmentsTypeController()
FIELDS_AS_PRIMARY_KEY = ['tag']
# Router ---------------------------------------------------------------------------------
router = APIRouter(prefix="/crud", tags=["CRUD dos diversos equipamentos"])

def connect_to_collection(category: str, type: str):
    # Verifica se existe a collection
    if not crud_handler.collection_exists(type):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Collection fornecida não existe")
    # Verifica se existe a categoria no controlador de schemas
    if not schema_controller.category_exists(category):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Categoria não existe no controlador de schemas. Fornecido: {category}")
    # Seta a categoria
    schema_controller.set_equip_category(category)
    # Verifica se existe o tipo de equipamento na categoria especificada no controlador de schemas   
    if not schema_controller.type_exists(type):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Tipo de equipamento fornecido não existe. Tipo fornecido: {type}")
    # Seta o tipo de equipamento
    schema_controller.set_equip_type(type)
    crud_handler.set_collection(type) # Conecta o crud_handler à collection associada

    return type

def decode_jsonify_query(query_param):
    if query_param:
        query_param = urllib.parse.unquote(query_param)
        try:
            query_param = json.loads(query_param)
        except:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parâmetro não pôde ser carregado como um dicionário")
    
    return query_param

def common_parameters(skip: Optional[int] = None, limit: Optional[int] = None, filter: str = None, sort: str = None, projection: List[str] = Query(None, alias="projection[]")):
    filter = decode_jsonify_query(filter)
    sort = decode_jsonify_query(sort)

    parameters = {"skip": skip, "limit": limit, "filter": filter, "sort": sort, "projection": projection}

    return parameters


def find_and_transform_date(documents_df, request_schema):
    documents = documents_df.copy()
    for prop in request_schema.schema()['properties']:
        if 'format' in request_schema.schema()['properties'][prop]:
            if request_schema.schema()['properties'][prop]['format'] == 'date':
                documents[prop] = documents[prop].apply(lambda x: date.fromisoformat(x).strftime("%d/%m/%Y") if not pd.isna(x) and x is not None else x)
    return documents


# Rotas ----------------------------------------------------------------------------------

@router.get("/{category}/{type}/download", summary="Baixa todos os documentos da rota em questão como um arquivo .csv", dependencies=[Depends(valid_user)])
def download_documents(type: str = Depends(connect_to_collection)):
    all_documents = crud_handler.find_all()[0]
    if len(all_documents) == 0:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="A tabela está vazia.")
        
    documents_df = pd.DataFrame.from_records(all_documents)
    current_schema = schema_controller.get_current_schema()

    documents_df = find_and_transform_date(documents_df=documents_df, request_schema=current_schema)

    csv_file = StringIO()
    documents_df.to_csv(csv_file, index=False, sep=';', encoding='latin')

    return StreamingResponse(
        iter([csv_file.getvalue()]),
        headers={"Content-Disposition": f"inline; filename=\"{type}.csv\""},
        media_type='text/csv'
    )

@router.get("/{category}/{type}/", summary="Obtém todos os documentos", dependencies=[Depends(connect_to_collection), Depends(valid_user)])
def get_documents(paginated: bool = False, getParameters: dict = Depends(common_parameters)):
    documents, _, __, total_documents = crud_handler.find_all(**getParameters)
    return {"documents": documents, "total": total_documents} if paginated else documents

@router.get("/{category}/{type}/{document_id}", dependencies=[Depends(connect_to_collection)])
def get_document(document_id: str):
    filter = {'_id': document_id}
    document, exists = crud_handler.find_one(filter)
    if not exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Documento com o id fornecido não existe")
    return document

@router.get("/{category}/{type}/unique/{col}", dependencies=[Depends(connect_to_collection), Depends(valid_user)])
def get_unique_values_in_col(col: str):
    uniques = crud_handler.find_unique(col)[0] # Devolve só o array
    return uniques

@router.post("/{category}/{type}/", summary="Cadastra um novo documento", dependencies=[Depends(connect_to_collection), Depends(valid_user)])
def post_document(document: dict = Depends(schema_controller)): # O depends naturalmente chama o método "call" da classe, o que nesse caso vai retornar o documento como um dict
    result = crud_handler.insert_one(document, fields_primary_key=FIELDS_AS_PRIMARY_KEY)
    return {"detail": "Documento inserido com sucesso", "_id": result[0]}

@router.put("/{category}/{type}/{document_id}", summary="Altera um documento existente", dependencies=[Depends(connect_to_collection), Depends(valid_user)])
def put_document(document_id: str, document: dict = Depends(schema_controller)):
    filter = {'_id': document_id}
    result = crud_handler.find_one_and_update(filter=filter, updated_document=document)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Documento com o id fornecido não existe")
    return {"detail": "Documento alterado com sucesso"}

@router.delete("/{category}/{type}/{document_id}", summary="Deleta um documento existente", dependencies=[Depends(connect_to_collection), Depends(valid_user)])
def delete_document(document_id: str):
    filter = {'_id': document_id}
    result = crud_handler.find_one_and_delete(filter=filter)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Documento com o id fornecido não existe")
    return {"detail": "Documento removido com sucesso"}

# ----------------------------------------------------------------------------------------
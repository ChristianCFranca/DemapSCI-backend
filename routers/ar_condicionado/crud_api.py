# Importa a classe de rotas do FastAPI e todas as dependências úteis dela
from re import S
from fastapi import Depends, Query, HTTPException, status
from fastapi import APIRouter as FastAPIRouter
from fastapi.responses import StreamingResponse
from auth import valid_user

# Pegar o json da Query
import urllib
import json

# Importa os typings para definir tipos de resposta esperados
from typing import Optional, List, Any, Callable

# Importa o crud_handler para a coleção atual
from database import crud_handler

# Para baixar como .csv
import pandas as pd
from datetime import date
from io import BytesIO, StringIO

# Classe que corrige o redirect 307 do starlette
class APIRouter(FastAPIRouter):
    def add_api_route(
            self, path: str, endpoint: Callable[..., Any], *,
            include_in_schema: bool = True, **kwargs: Any
            ) -> None:
        if path.endswith("/"):
            alternate_path = path[:-1]
        else:           
            alternate_path = path + "/"
        super().add_api_route(                                                 
            alternate_path, endpoint, include_in_schema=False, **kwargs)
        return super().add_api_route(
            path, endpoint, include_in_schema=include_in_schema, **kwargs)

# Define nosso router
router = APIRouter(prefix="/ar-condicionado", tags=["Fan Coils"])

# Schemas --------------------------------------------------------------------------------
from .schemas import FanCoilRequest, ChillerRequest, TorreRequest, BombaRequest, SplitRequest, SelfRequest, VRFCondRequest, VRFEvapRequest

# Dependências ---------------------------------------------------------------------------

class ACTypeEquipmentsDict:
    def __init__(self, ac_type: str):
        self.ac_type = ac_type
        self.ROUTE_SCHEMAS_DICT = {
            'fancoils': FanCoilRequest,
            'chillers': ChillerRequest,
            'torres': TorreRequest,
            'bombas': BombaRequest,
            'splits': SplitRequest,
            'selfs': SelfRequest,
            'vrfconds': VRFCondRequest,
            'vrfevaps': VRFEvapRequest,
        }

    def set_ac_type(self, ac_type):
        self.ac_type = ac_type

    def __call__(self, document: dict):
        
        document = self.ROUTE_SCHEMAS_DICT[self.ac_type](**document)
        
        if document.dataFabricacao:
            document.dataFabricacao = str(document.dataFabricacao)
        if document.dataInstalacao:
            document.dataInstalacao = str(document.dataInstalacao)

        return document.dict() # É transformado novamente pois isso filtra algumas keys perigosas como _id
    
ac_type_equipments_dict = ACTypeEquipmentsDict('fancoils')

FIELDS_AS_PRIMARY_KEY = ['tag']

def check_if_valid_collection_then_connect(ac_type: str):
    if not crud_handler.collection_exists(ac_type) or ac_type not in ac_type_equipments_dict.ROUTE_SCHEMAS_DICT:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Collection fornecida não existe")
    crud_handler.set_collection(ac_type) # Conecta o crud_handler à collection
    ac_type_equipments_dict.set_ac_type(ac_type)
    return ac_type

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

@router.get("/{ac_type}/download", summary="Baixa todos os documentos da rota em questão como um arquivo .csv", dependencies=[Depends(valid_user)])
def download_documents(ac_type: str = Depends(check_if_valid_collection_then_connect)):
    all_documents = crud_handler.find_all()[0]
    if len(all_documents) == 0:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="A tabela está vazia.")
        
    documents_df = pd.DataFrame.from_records(all_documents)
    current_schema = ac_type_equipments_dict.ROUTE_SCHEMAS_DICT[ac_type_equipments_dict.ac_type]

    documents_df = find_and_transform_date(documents_df=documents_df, request_schema=current_schema)

    xlsx_file = BytesIO()
    with pd.ExcelWriter(xlsx_file) as writer:
        documents_df.to_excel(writer, index=False, encoding='utf-8')
        writer.save()

    return StreamingResponse(
        iter([xlsx_file.getvalue()]),
        media_type='application/xml'
    )

@router.get("/{ac_type}/", summary="Obtém todos os documentos", dependencies=[Depends(check_if_valid_collection_then_connect), Depends(valid_user)])
def get_documents(paginated: bool = False, getParameters: dict = Depends(common_parameters)):
    documents, _, __, total_documents = crud_handler.find_all(**getParameters)
    return {"documents": documents, "total": total_documents} if paginated else documents

@router.get("/{ac_type}/{document_id}", dependencies=[Depends(check_if_valid_collection_then_connect)])
def get_document(document_id: str):
    filter = {'_id': document_id}
    document, exists = crud_handler.find_one(filter)
    if not exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Documento com o id fornecido não existe")
    return document

@router.get("/{ac_type}/unique/{col}", dependencies=[Depends(check_if_valid_collection_then_connect), Depends(valid_user)])
def get_unique_values_in_col(col: str):
    uniques = crud_handler.find_unique(col)[0] # Devolve só o array
    return uniques

@router.post("/{ac_type}/", summary="Cadastra um novo documento", dependencies=[Depends(check_if_valid_collection_then_connect), Depends(valid_user)])
def post_document(document: dict = Depends(ac_type_equipments_dict)):
    result = crud_handler.insert_one(document, fields_primary_key=FIELDS_AS_PRIMARY_KEY)
    return {"detail": "Documento inserido com sucesso", "_id": result[0]}

@router.put("/{ac_type}/{document_id}", summary="Altera um documento existente", dependencies=[Depends(check_if_valid_collection_then_connect), Depends(valid_user)])
def put_document(document_id: str, document: dict = Depends(ac_type_equipments_dict)):
    filter = {'_id': document_id}
    result = crud_handler.find_one_and_update(filter=filter, updated_document=document)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Documento com o id fornecido não existe")
    return {"detail": "Documento alterado com sucesso"}

@router.delete("/{ac_type}/{document_id}", summary="Deleta um documento existente", dependencies=[Depends(check_if_valid_collection_then_connect), Depends(valid_user)])
def delete_document(document_id: str):
    filter = {'_id': document_id}
    result = crud_handler.find_one_and_delete(filter=filter)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Documento com o id fornecido não existe")
    return {"detail": "Documento removido com sucesso"}
# ----------------------------------------------------------------------------------------
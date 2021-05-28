from fastapi import status, HTTPException
import pymongo
from bson.errors import InvalidId
from bson import ObjectId

# Para o type annotations
from typing import Tuple, List

class DBCollectionCrudHandler:
    def __init__(self, db: pymongo.database.Database):
        if not isinstance(db, pymongo.database.Database):
            raise Exception("Objeto Database não é do tipo correto")
        self.db = db
        self.collection = None

    def set_collection(self, collection: str):
        if not isinstance(collection, str):
            raise Exception("Collection deve ser uma string")
        self.collection = self.db[collection]

    def collection_exists(self, ac_type) -> bool:
        return ac_type in self.db.list_collection_names()

    def map_documents_ids(self, documents: List[dict]) -> List[dict]:
        """
        Mapeia os _ids do documentos de ObjectIds para strings
        """
        for document in documents:
            document['_id'] = str(document['_id'])
        return documents

    def check_and_correct_filter(self, filter):
        if not isinstance(filter, dict):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Filtro não é um dicionário")
        if '_id' in filter and not isinstance(filter['_id'], ObjectId):
            try:
                filter['_id'] = ObjectId(filter['_id'])
            except InvalidId:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Formato incorreto para o Id fornecido")
        return filter

    def check_projection(self, projection):
        if not isinstance(projection, list):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Projection não é uma lista")
        for proj in projection:
            if not isinstance(proj, str):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Algumas das projeções não é uma string")

    def insert_one(self, document: dict, fields_primary_key: List[str] = None) -> Tuple[str, bool]:
        """
        Insere um novo documento na coleção. Retorna o id inserido como uma string e se o resultado foi None
        """
        if not isinstance(document, dict):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Documento deve ser do tipo dicionário")

        if fields_primary_key:
            for field_primary_key in fields_primary_key:
                if field_primary_key not in document:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Campo \'{field_primary_key}\' não existe no documento em questão")
                exists = self.find_one({field_primary_key: document[field_primary_key]})[1] # {'_id': av6C123As512FF00123} exemplo
                if exists:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"O documento apresenta um valor de um dos campos de chave primária ({field_primary_key}) já existente no banco de dados")

        result = self.collection.insert_one(document)
        return str(result.inserted_id), result is not None

    def insert_many(self, documents: List[dict]) -> Tuple[List[str], bool, int]:
        """
        Insere vários documentos na coleção. Retorna is ids inseridos, se algum id foi de fato inserido e a quantidade de id's inseridos
        """
        if not isinstance(documents, list):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Documento deve ser do tipo lista")
        if len(documents) == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Lista de documentos está vazia")
        try:
            len(list(filter(lambda doc: isinstance(dict, doc), documents))) != len(documents)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Existem itens na lista que não são documentos dict")

        result = self.collection.insert_many(documents)
        inserted_ids = []
        if result is not None:
            inserted_ids = [str(inserted_id) for inserted_id in result.inserted_ids]
        return inserted_ids, result is not None, len(inserted_ids)

    def find_all(self, skip: int = None, limit: int = None, filter: dict = None, sort: List[Tuple[str, int]] = None, projection: List[str] = None):
        """
        Retorna todos os documentos, se algum documento foi encontrado e o tamanho dos documentos opcionalmente utilizando um filtro. Os resultados são devolvidos em bateladas
        """
        if filter:
            filter = self.check_and_correct_filter(filter)
        if projection:
            self.check_projection(projection)
        if isinstance(sort, dict):
            sort = list(sort.items())

        if skip and limit:
            documents = list(self.collection.find(filter=filter, projection=projection, sort=sort).skip(skip).limit(limit)) # Paginação filtrada ordenada limitada
        elif limit:
            documents = list(self.collection.find(filter=filter, projection=projection, sort=sort).limit(limit)) # Paginação filtrada ordenada limitada
        else:
            documents = list(self.collection.find(filter=filter, projection=projection, sort=sort)) # Paginação filtrada ordenada total

        documents = self.map_documents_ids(documents=documents)
        total_len_documents = self.collection.estimated_document_count(maxTimeMS=5000) # 5 segundos

        return documents, len(documents) != 0, len(documents), total_len_documents

    def find_unique(self, col_to_check: str = None):
        """
        Retorna uma lista de todos os itens únicos de uma coluna
        """
        uniques = list(self.collection.find().distinct(col_to_check)) # Paginação filtrada ordenada total

        return uniques, len(uniques) != 0, len(uniques)

    def find_one(self, filter: dict = None) -> Tuple[dict, bool]:
        """
        Retorna o primeiro documento encontrado e se algum documento foi encontrado utilizando opcionalmente um filtro
        """
        if filter:
            filter = self.check_and_correct_filter(filter)

        document = self.collection.find_one(filter)
        if document is not None:
            document['_id'] = str(document['_id'])

        return document, document is not None

    def find_one_and_replace(self, filter: dict, replacement: dict) -> bool:
        """
        Encontra o primeiro documento que satisfaz um filtro e o substitui por um novo documento. Retorna um booleano indicando se alguma substituição ocorreu
        """
        filter = self.check_and_correct_filter(filter)

        if not isinstance(replacement, dict):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Replacement não é um dicionário")

        result = self.collection.find_one_and_replace(filter, replacement)
        return result is not None

    def find_one_and_update(self, filter: dict, updated_document: dict) -> bool:
        """
        Encontra o primeiro documento que satisfaz um filtro e o atualiza. Retorna um booleano indicando se algum documento foi encontrado
        """
        filter = self.check_and_correct_filter(filter)

        if not isinstance(updated_document, dict):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Replacement não é um dicionário")

        result = self.collection.find_one_and_update(filter, {'$set': updated_document})
        return result is not None

    def find_one_and_delete(self, filter: dict) -> bool:
        """
        Encontra o primeiro documento que satisfaz um filtro e o deleta. Retorna um booleano indicando se algum documento foi encontrado
        """
        filter = self.check_and_correct_filter(filter)

        result = self.collection.find_one_and_delete(filter)
        return result is not None

    def update_many(self, filter: dict, update_to_all_documents: dict) -> Tuple[int, bool]:
        """
        Encontra todos os documento que satisfazem um filtro e os atualizam. Retorna um booleano indicando se algum documento foi atualizado
        """
        filter = self.check_and_correct_filter(filter)

        if not isinstance(update_to_all_documents, dict):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Replacement não é um dicionário")

        result = self.collection.update_many(filter, {'$set': update_to_all_documents})
        return result.modified_count, result.modified_count != 0



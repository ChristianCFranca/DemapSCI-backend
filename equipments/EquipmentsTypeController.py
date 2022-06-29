# Obtem todas as definições dos tipos diferentes de equipamentos
from numpy import isin
from .ar_condicionado.schemas import ROUTE_SCHEMAS_DICT as ac_dict
from .energia.schemas import ROUTE_SCHEMAS_DICT as energy_dict

# Para verificação de erros
from pydantic.error_wrappers import ValidationError
from fastapi import HTTPException, status

# Para correção dos Schemas
from datetime import date

# O controlador é a classe que define o caminho correto de uma definição de um equipamento
class EquipmentsTypeController:
    def __init__(self):
        self.category = 'ar-condicionado'
        self.tipo = 'fancoils'
        self.ROUTE_SCHEMAS_DICT = {
            'ar-condicionado': ac_dict,
            'energia': energy_dict
        }

    def category_exists(self, category):
        return category in self.ROUTE_SCHEMAS_DICT

    def type_exists(self, tipo):
        return tipo in self.ROUTE_SCHEMAS_DICT[self.category]

    def set_equip_category(self, category):
        self.category = category

    def set_equip_type(self, tipo):
        self.tipo = tipo

    def get_current_schema(self):
        return self.ROUTE_SCHEMAS_DICT[self.category][self.tipo]

    def __call__(self, document: dict):
        try:
            document = self.ROUTE_SCHEMAS_DICT[self.category][self.tipo](**document)
        except ValidationError as e: # Isso é apenas uma forma de propagar a string do erro original de validação em cima de um status 400 (do contrário daria status 500)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

        # Correção do datetime
        for key in document.__annotations__.keys():
            if isinstance(document.__getattribute__(key), date):
                document.__setattr__(key, str(document.__getattribute__(key)))

        return document.dict() # É transformado novamente pois isso filtra algumas keys perigosas como _id
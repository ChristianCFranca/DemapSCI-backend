from pydantic import BaseModel
from fastapi import Body
from typing import Optional
from datetime import date

class GeradorRequest(BaseModel):
    tag: str
    fabricanteAlternador: Optional[str] = Body(None)
    fabricanteMotor: Optional[str] = Body(None)
    fabricanteGMG: Optional[str] = Body(None)
    modeloGMG: Optional[str] = Body(None)
    potencia: Optional[float] = Body(None)
    capTanque: Optional[float] = Body(None)
    fabricanteBateria: Optional[str] = Body(None)
    modeloBateria: Optional[str] = Body(None)
    capacidadeBateria: Optional[str] = Body(None)
    dataInstBateria: Optional[date] = Body(None)
    tipoArrefecimento: Optional[str] = Body(None)
    fatPot: Optional[float] = Body(None)
    tensaoSaida: Optional[float] = Body(None)
    local: str
    dataFabricacao: Optional[date] = Body(None)
    dataInstalacao: Optional[date] = Body(None)
    infAdicional: Optional[str] = Body(None)

ROUTE_SCHEMAS_DICT = {
            'geradores': GeradorRequest,
        }
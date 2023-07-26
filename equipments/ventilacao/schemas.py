from pydantic import BaseModel
from fastapi import Body
from typing import Optional
from datetime import date

class VentiladorRequest(BaseModel):
    tag: str
    pavimento: str
    torre: str
    modo: str
    ala: Optional[str] = Body(None)
    fabricante: Optional[str] = Body(None)
    modelo: Optional[str] = Body(None)
    vazao: Optional[float] = Body(None)
    pressaoEstaticaDisponivel: Optional[float] = Body(None)
    tipo: Optional[str] = Body(None)
    potenciaMotor: Optional[float] = Body(None)
    polia: Optional[str] = Body(None)
    tensao: Optional[int] = Body(None)
    tipoEnergia: Optional[str] = Body(None)
    dataFabricacao: Optional[date] = Body(None)
    dataInstalacao: Optional[date] = Body(None)
    local: str
    infAdicional: Optional[str] = Body(None)

ROUTE_SCHEMAS_DICT = {
            'ventiladores': VentiladorRequest
        }
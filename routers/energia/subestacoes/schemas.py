from fastapi import Body, FastAPI

from typing import Optional

from pydantic import BaseModel

# from datetime import date

class SubestacaoRequest(BaseModel):
    tag: str
    disjuntorGeral: Optional[str] = Body(None)
    tipoQuadro: Optional[str] = Body(None)
    quantidadeCircuitos: Optional[int] = Body(None)
    circuito1: Optional[str] = Body(None)
    aplCircuito1: Optional[str] = Body(None)
    circuito2: Optional[str] = Body(None)
    aplCircuito2: Optional[str] = Body(None)
    circuito3: Optional[str] = Body(None)
    aplCircuito3: Optional[str] = Body(None)
    circuitoXX: Optional[str] = Body(None)
    aplCircuitoXX: Optional[str] = Body(None)
    demandaContratada: Optional[float] = Body(None)
    concessionaria: Optional[str] = Body(None)
    infAdicional: Optional[str] = Body(None)
    #dataX: Optional[date] = Body(None)

class SubestacaoResponse(SubestacaoRequest):
    id: int

    class Config:
        orm_mode = True

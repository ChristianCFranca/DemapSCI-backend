from fastapi import Body, FastAPI

from typing import Optional

from pydantic import BaseModel

from datetime import date

class FanCoilRequest(BaseModel):
    tag: str
    pavimento: str
    torre: str
    fabricante: Optional[str] = Body(None)
    modelo: Optional[str] = Body(None)
    vazao: Optional[float] = Body(None)
    filtro: Optional[str] = Body(None)
    cargaTermica: Optional[float] = Body(None)
    pressaoEstaticaDisponivel: Optional[float] = Body(None)
    tipoVentilador: Optional[str] = Body(None)
    modeloVentilador: Optional[str] = Body(None)
    potenciaMotor: Optional[float] = Body(None)
    polia: Optional[str] = Body(None)
    tensao: Optional[int] = Body(None)
    altura: Optional[int] = Body(None)
    largura: Optional[int] = Body(None)
    comprimento: Optional[int] = Body(None)
    tipoEnergia: Optional[str] = Body(None)
    dataFabricacao: Optional[date] = Body(None)
    dataInstalacao: Optional[date] = Body(None)
    infAdicional: Optional[str] = Body(None)


class FanCoilResponse(FanCoilRequest):
    id: int

    class Config:
        orm_mode = True

from pydantic import BaseModel
from fastapi import Body
from typing import Optional
from datetime import date

class FanCoilRequest(BaseModel):
    tag: str
    pavimento: str
    torre: str
    fabricante: Optional[str] = Body(None)
    modelo: Optional[str] = Body(None)
    vazao: Optional[float] = Body(None)
    filtro: Optional[str] = Body(None)
    alturaDoFiltro: Optional[float] = Body(None)
    larguraDoFiltro: Optional[float] = Body(None)
    espessuraDoFiltro: Optional[float] = Body(None)
    cargaTermica: Optional[float] = Body(None)
    pressaoEstaticaDisponivel: Optional[float] = Body(None)
    perdaDeCarga: Optional[float] = Body(None)
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
    local: str
    infAdicional: Optional[str] = Body(None)

class ChillerRequest(BaseModel):
    tag: str
    modelo: Optional[str] = Body(None)
    fabricante: Optional[str] = Body(None)
    vazaoEvap: Optional[float] = Body(None)
    vazaoCond: Optional[float] = Body(None)
    tensao: Optional[int] = Body(None)
    potenciaMotor: Optional[float] = Body(None)
    cargaTermica: Optional[float] = Body(None)
    correnteNominal: Optional[float] = Body(None)
    tempEntradaEvap: Optional[float] = Body(None)
    tempSaidaEvap: Optional[float] = Body(None)
    tempEntradaCond: Optional[float] = Body(None)
    tempSaidaCond: Optional[float] = Body(None)
    numeroSerie: Optional[str] = Body(None)
    tipoEnergia: Optional[str] = Body(None)
    tipoOleo: Optional[str] = Body(None)
    tipoGas: Optional[str] = Body(None)
    dataFabricacao: Optional[date] = Body(None)
    dataInstalacao: Optional[date] = Body(None)
    local: str
    infAdicional: Optional[str] = Body(None)

class TorreRequest(BaseModel):
    tag: str
    modelo: Optional[str] = Body(None)
    fabricante: Optional[str] = Body(None)
    vazaoAr: Optional[float] = Body(None)
    vazaoAgua: Optional[float] = Body(None)
    tensao: Optional[int] = Body(None)
    potenciaMotor: Optional[float] = Body(None)
    cargaTermica: Optional[float] = Body(None)
    correnteNominal: Optional[float] = Body(None)
    tempEntrada: Optional[float] = Body(None)
    tempSaida: Optional[float] = Body(None)
    numeroSerie: Optional[str] = Body(None)
    tipoEnergia: Optional[str] = Body(None)
    dataFabricacao: Optional[date] = Body(None)
    dataInstalacao: Optional[date] = Body(None)
    local: str
    infAdicional: Optional[str] = Body(None)

class BombaRequest(BaseModel):
    tag: str
    modelo: Optional[str] = Body(None)
    fabricante: Optional[str] = Body(None)
    vazao: Optional[float] = Body(None)
    tensao: Optional[int] = Body(None)
    potenciaMotor: Optional[float] = Body(None)
    correnteNominal: Optional[float] = Body(None)
    numeroSerie: Optional[str] = Body(None)
    tipoEnergia: Optional[str] = Body(None)
    pressao: Optional[float] = Body(None)
    alturaMonometrica: Optional[float] = Body(None)
    dataFabricacao: Optional[date] = Body(None)
    dataInstalacao: Optional[date] = Body(None)
    local: str
    infAdicional: Optional[str] = Body(None)

class SplitRequest(BaseModel):
    tag: str
    pavimento: str
    torre: int
    modeloCond: Optional[str] = Body(None)
    modeloEvap: Optional[str] = Body(None)
    fabricante: Optional[str] = Body(None)
    tensao: Optional[int] = Body(None)
    potEvap: Optional[float] = Body(None)
    potCond: Optional[float] = Body(None)
    cargaTermica: Optional[float] = Body(None)
    tipoGas: Optional[str] = Body(None)
    tipoFiltro: Optional[str] = Body(None)
    numeroSerie: Optional[str] = Body(None)
    dataFabricacao: Optional[date] = Body(None)
    dataInstalacao: Optional[date] = Body(None)
    local: str
    infAdicional: Optional[str] = Body(None)

class SelfRequest(BaseModel):
    tag: str
    pavimento: str
    torre: int
    modeloCond: Optional[str] = Body(None)
    modeloEvap: Optional[str] = Body(None)
    fabricante: Optional[str] = Body(None)
    tensao: Optional[int] = Body(None)
    potEvap: Optional[float] = Body(None)
    potCond: Optional[float] = Body(None)
    cargaTermica: Optional[float] = Body(None)
    tipoGas: Optional[str] = Body(None)
    filtro: Optional[str] = Body(None)
    alturaFiltro: Optional[float] = Body(None)
    larguraFiltro: Optional[float] = Body(None)
    espessuraFiltro: Optional[float] = Body(None)
    numeroSerie: Optional[str] = Body(None)
    dataFabricacao: Optional[date] = Body(None)
    dataInstalacao: Optional[date] = Body(None)
    local: str
    infAdicional: Optional[str] = Body(None)

class VRFCondRequest(BaseModel):
    tag: str
    tagEvap: Optional[str] = Body(None)
    pavimento: str
    torreAla: str
    modelo: Optional[str] = Body(None)
    fabricante: Optional[str] = Body(None)
    tensao: Optional[int] = Body(None)
    potenciaMotor: Optional[float] = Body(None)
    cargaTermica: Optional[float] = Body(None)
    tipoFiltro: Optional[str] = Body(None)
    tipoEnergia: Optional[str] = Body(None)
    dataFabricacao: Optional[date] = Body(None)
    dataInstalacao: Optional[date] = Body(None)
    local: str
    infAdicional: Optional[str] = Body(None)

class VRFEvapRequest(BaseModel):
    tag: str
    tagCond: str
    pavimento: str
    torreAla: str
    modelo: Optional[str] = Body(None)
    fabricante: Optional[str] = Body(None)
    tensao: Optional[int] = Body(None)
    potenciaMotor: Optional[float] = Body(None)
    cargaTermica: Optional[float] = Body(None)
    tipoFiltro: Optional[str] = Body(None)
    tipoEnergia: Optional[str] = Body(None)
    dataFabricacao: Optional[date] = Body(None)
    dataInstalacao: Optional[date] = Body(None)
    local: str
    infAdicional: Optional[str] = Body(None)
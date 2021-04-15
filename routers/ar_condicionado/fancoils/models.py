from sqlalchemy import Column, Integer, String, Numeric, Integer, Date
from database import Base

# Classes Modelos -------------------------------------------------

class FanCoil(Base):
    __tablename__ = "fancoils"

    id = Column(Integer, primary_key=True, index=True)
    tag = Column(String(50), index=True)
    pavimento = Column(String(20))
    torre = Column(String(20))
    fabricante = Column(String(50), nullable=True)
    modelo = Column(String(50), nullable=True)
    vazao = Column(Numeric)
    filtro = Column(String(50), nullable=True)
    cargaTermica = Column(Numeric)
    pressaoEstaticaDisponivel = Column(Numeric)
    tipoVentilador = Column(String(50), nullable=True)
    modeloVentilador = Column(String(50), nullable=True)
    potenciaMotor = Column(Numeric)
    polia = Column(String(50), nullable=True)
    tensao = Column(Integer)
    altura = Column(Integer, nullable=True)
    largura = Column(Integer, nullable=True)
    comprimento = Column(Integer, nullable=True)
    tipoEnergia = Column(String(50), nullable=True)
    dataFabricacao = Column(Date, nullable=True)
    dataInstalacao = Column(Date, nullable=True)
    infAdicional = Column(String(200), nullable=True)
    

    
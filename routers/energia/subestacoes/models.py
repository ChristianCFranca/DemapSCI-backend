from sqlalchemy import Column, Integer, String, Numeric, Integer #, Date
from database import Base

# Classes Modelos -------------------------------------------------

class Subestacao(Base):
    __tablename__ = "subestacoes"

    id = Column(Integer, primary_key=True, index=True)
    tag = Column(String(50), index=True)
    disjuntorGeral = Column(String(50), nullable=True)
    tipoQuadro = Column(String(50), nullable=True)
    quantidadeCircuitos = Column(Integer, nullable=True)
    circuito1 = Column(String(50), nullable=True)
    aplCircuito1 = Column(String(50), nullable=True)
    circuito2 = Column(String(50), nullable=True)
    aplCircuito2 = Column(String(50), nullable=True)
    circuito3 = Column(String(50), nullable=True)
    aplCircuito3 = Column(String(50), nullable=True)
    circuitoXX = Column(String(50), nullable=True)
    aplCircuitoXX = Column(String(50), nullable=True)
    demandaContratada = Column(Numeric, nullable=True)
    concessionaria = Column(String(50), nullable=True)
    infAdicional = Column(String(200), nullable=True)
    #dataX = Column(Date, nullable=True)
    
    

    
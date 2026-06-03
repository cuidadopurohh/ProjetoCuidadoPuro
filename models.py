from sqlalchemy import Column, Integer, String, Float, DateTime
from database import Base
from datetime import datetime


class Cliente(Base):
    """Modelo de Cliente - Representa um cliente cadastrado"""
   
    # Nome da tabela no banco
    __tablename__ = "Clientes"
   
    # Colunas da tabela (campos da ficha)
    id_cliente = Column(Integer, primary_key=True, index=True)
    nome_cliente = Column(String(100), nullable=False)  # Não pode ser vazio
    rg_cliente = Column(String(15), nullable=False)
    cpf_cliente = Column(String(11), nullable=False)
    endereco_cliente = Column(String(150), nullable=False) 
    telefone_cliente = Column(String(20), nullable=False)
    idade_cliente = Column(String(2), nullable=False) 
    data_cadastro = Column(DateTime, default=datetime.utcnow)
    email_cliente = Column(String(100), nullable=False, unique=True)
    senha_cliente = Column(String(100), nullable=False) 
   
    def __repr__(self):
        """Como o cliente aparece quando printado"""
        return f"<Cliente {self.nome_cliente}>"

class Profissional(Base):
    """Modelo de Profissional - Representa um profissional cadastrado"""
   
    # Nome da tabela no banco
    __tablename__ = "Profissionais"
   
    # Colunas da tabela (campos da ficha)
    id_profissional = Column(Integer, primary_key=True, index=True)
    nome_profissional = Column(String(100), nullable=False)  # Não pode ser vazio
    rg_profissional = Column(String(15), nullable=False)
    cpf_profissional = Column(String(11), nullable=False)
    endereco_profissional = Column(String(150), nullable=False) 
    telefone_profissional = Column(String(20), nullable=False)
    idade_profissional = Column(String(2), nullable=False) 
    data_cadastro = Column(DateTime, default=datetime.utcnow)
    email_profissional = Column(String(100), nullable=False, unique=True)
    senha_profissional = Column(String(100), nullable=False) 
   
    def __repr__(self):
        """Como o profissional aparece quando printado"""
        return f"<Profissional {self.nome_profissional}>"

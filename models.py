from datetime import datetime
from database import Base
from sqlalchemy import Column, DateTime, Integer, String, Text


class Cliente(Base):
    """Modelo de Cliente - Representa um cliente cadastrado"""

    __tablename__ = "Clientes"

    id_cliente = Column(Integer, primary_key=True, index=True)
    nome_cliente = Column(String(100), nullable=False)
    rg_cliente = Column(String(15), nullable=False)
    cpf_cliente = Column(String(11), nullable=False)
    endereco_cliente = Column(String(150), nullable=False)
    telefone_cliente = Column(String(20), nullable=False)
    idade_cliente = Column(String(2), nullable=False)
    data_cadastro = Column(DateTime, default=datetime.utcnow)
    email_cliente = Column(String(100), nullable=False, unique=True)
    senha_cliente = Column(String(100), nullable=False)

    # === Novos campos vindos do formulário de saúde (Frontend) ===
    nome_paciente = Column(String(100), nullable=True)
    idade_paciente = Column(Integer, nullable=True)
    condicao_principal = Column(String(150), nullable=True)
    nivel_suporte = Column(String(50), nullable=True)
    observacoes_cuidados = Column(Text, nullable=True)  # Text para observações longas

    def __repr__(self):
        return f"<Cliente {self.nome_cliente}>"


class Profissional(Base):
    """Modelo de Profissional - Representa um profissional cadastrado"""

    __tablename__ = "Profissionais"

    id_profissional = Column(Integer, primary_key=True, index=True)
    nome_profissional = Column(String(100), nullable=False)
    rg_profissional = Column(String(15), nullable=False)
    cpf_profissional = Column(String(11), nullable=False)
    endereco_profissional = Column(String(150), nullable=False)
    telefone_profissional = Column(String(20), nullable=False)
    idade_profissional = Column(String(2), nullable=False)
    data_cadastro = Column(DateTime, default=datetime.utcnow)
    email_profissional = Column(String(100), nullable=False, unique=True)
    senha_profissional = Column(String(100), nullable=False)

    # === Novos campos vindos do formulário profissional (Frontend) ===
    registro_profissional = Column(String(50), nullable=True)
    tempo_experiencia = Column(String(50), nullable=True)
    especialidade_principal = Column(String(100), nullable=True)
    procedimentos_dispositivos = Column(String(200), nullable=True)
    detalhes_capacitacao = Column(Text, nullable=True)

    def __repr__(self):
        return f"<Profissional {self.nome_profissional}>"

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, SecretStr, validator


# ==================== TABELAS CLIENTES ====================
class ClienteBase(BaseModel):
    """Schema base - campos comuns"""

    nome_cliente: str = Field(
        ..., min_length=1, max_length=100, description="Nome do cliente"
    )
    rg_cliente: str = Field(..., description="Digite seu RG")
    cpf_cliente: str = Field(..., description="Digite seu CPF")
    endereco_cliente: str = Field(
        ..., min_length=1, max_length=150, description="Endereço"
    )
    telefone_cliente: str = Field(..., description="Telefone")
    idade_cliente: str = Field(..., description="Idade do cliente responsável")
    email_cliente: str = Field(
        ..., min_length=1, max_length=100, description="E-mail"
    )
    senha_cliente: SecretStr = Field(
        ..., min_length=6, max_length=100, description="Senha"
    )

    # Novos campos opcionais do Paciente vinculados ao Cliente
    nome_paciente: Optional[str] = None
    idade_paciente: Optional[int] = None
    condicao_principal: Optional[str] = None
    nivel_suporte: Optional[str] = None
    observacoes_cuidados: Optional[str] = None

    @validator("nome_cliente")
    def nome_nao_pode_ser_vazio(cls, v):
        if not v or v.strip() == "":
            raise ValueError("Nome não pode ser vazio")
        return v.strip()

    @validator("email_cliente")
    def email_nao_pode_ser_vazio(cls, v):
        if not v or v.strip() == "":
            raise ValueError("E-mail não pode ser vazio")
        return v.strip()

    @validator("senha_cliente")
    def senha_nao_pode_ser_vazio(cls, v):
        texto_senha = (
            v.get_secret_value() if hasattr(v, "get_secret_value") else v
        )
        if not texto_senha or texto_senha.strip() == "":
            raise ValueError("Senha não pode ser vazia")
        return v


class ClienteCreate(ClienteBase):
    """Schema para CRIAR Cliente"""

    pass


class ClienteUpdate(BaseModel):
    """Schema para ATUALIZAR clientes (todos os campos são opcionais)"""

    nome_cliente: Optional[str] = None
    rg_cliente: Optional[str] = None
    cpf_cliente: Optional[str] = None
    endereco_cliente: Optional[str] = None
    telefone_cliente: Optional[str] = None
    idade_cliente: Optional[str] = None
    email_cliente: Optional[str] = None
    senha_cliente: Optional[SecretStr] = None

    nome_paciente: Optional[str] = None
    idade_paciente: Optional[int] = None
    condicao_principal: Optional[str] = None
    nivel_suporte: Optional[str] = None
    observacoes_cuidados: Optional[str] = None


class ClienteResponse(ClienteBase):
    """Schema para LER clientes"""

    id_cliente: int
    data_cadastro: datetime

    class Config:
        from_attributes = True


# ==================== TABELAS PROFISSIONAIS ====================


class ProfissionalBase(BaseModel):
    """Schema base - campos comuns"""

    nome_profissional: str = Field(
        ..., min_length=1, max_length=100, description="Nome do profissional"
    )
    rg_profissional: str = Field(..., description="Digite seu RG")
    cpf_profissional: str = Field(..., description="Digite seu CPF")
    endereco_profissional: str = Field(
        ..., min_length=1, max_length=150, description="Endereço"
    )
    telefone_profissional: str = Field(..., description="Telefone")
    idade_profissional: str = Field(..., description="Idade")
    email_profissional: str = Field(
        ..., min_length=1, max_length=100, description="E-mail"
    )
    senha_profissional: SecretStr = Field(
        ..., min_length=6, max_length=100, description="Senha"
    )

    # Novos campos opcionais do questionário profissional
    registro_profissional: Optional[str] = None
    tempo_experiencia: Optional[str] = None
    especialidade_principal: Optional[str] = None
    procedimentos_dispositivos: Optional[str] = None
    detalhes_capacitacao: Optional[str] = None

    @validator("nome_profissional")
    def nome_nao_pode_ser_vazio(cls, v):
        if not v or v.strip() == "":
            raise ValueError("Nome não pode ser vazio")
        return v.strip()

    @validator("email_profissional")
    def email_nao_pode_ser_vazio(cls, v):
        if not v or v.strip() == "":
            raise ValueError("E-mail não pode ser vazio")
        return v.strip()

    @validator("senha_profissional")
    def senha_nao_pode_ser_vazio(cls, v):
        texto_senha = (
            v.get_secret_value() if hasattr(v, "get_secret_value") else v
        )
        if not texto_senha or texto_senha.strip() == "":
            raise ValueError("Senha não pode ser vazia")
        return v


class ProfissionalCreate(ProfissionalBase):
    """Schema para CRIAR Profissional"""

    pass


class ProfissionalUpdate(BaseModel):
    """Schema para ATUALIZAR profissionais (todos os campos são opcionais)"""

    nome_profissional: Optional[str] = None
    rg_profissional: Optional[str] = None
    cpf_profissional: Optional[str] = None
    endereco_profissional: Optional[str] = None
    telefone_profissional: Optional[str] = None
    idade_profissional: Optional[str] = None
    email_profissional: Optional[str] = None
    senha_profissional: Optional[SecretStr] = None

    registro_profissional: Optional[str] = None
    tempo_experiencia: Optional[str] = None
    especialidade_principal: Optional[str] = None
    procedimentos_dispositivos: Optional[str] = None
    detalhes_capacitacao: Optional[str] = None


class ProfissionalResponse(ProfissionalBase):
    """Schema para LER profissionais"""

    id_profissional: int
    data_cadastro: datetime

    class Config:
        from_attributes = True

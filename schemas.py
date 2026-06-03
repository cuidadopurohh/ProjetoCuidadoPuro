from pydantic import BaseModel, Field, validator, SecretStr 
from datetime import datetime
from typing import Optional

# ==================== TABELAS CLIENTES ====================
class ClienteBase(BaseModel):
    """Schema base - campos comuns"""
    nome_cliente: str = Field(..., min_length=1, max_length=100, description="Nome do cliente")
    rg_cliente: float = Field(...,gt=0, description="Digite seu RG")
    cpf_cliente: float = Field(..., gt=0, description="Digite seu CPF")
    endereco_cliente: str = Field(..., min_length=1, max_length=150, description="Endereço")
    telefone_cliente: float = Field(..., gt=0, description="Telefone")
    idade_cliente: int = Field(..., gt=0, description="Data de Nascimento")
    email_cliente: str = Field(..., min_length=1, max_length=100, description="E-mail")
    senha_cliente: SecretStr = Field(..., min_length=6, max_length=100, description="Senha")
        
    @validator('nome_cliente')
    def nome_nao_pode_ser_vazio(cls, v):
        if not v or v.strip() == "":
            raise ValueError('Nome não pode ser vazio')
        return v.strip()
    
    @validator('email_cliente')
    def email_nao_pode_ser_vazio(cls, v):
        if not v or v.strip() == "":
            raise ValueError('E-mail não pode ser vazio')
        return v.strip()
        
    
    @validator('senha_cliente')
    def senha_nao_pode_ser_vazio(cls, v):
        texto_senha = v.get_secret_value() if hasattr(v, 'get_secret_value') else v
        if not texto_senha or texto_senha.strip() == "":
            raise ValueError('Senha não pode ser vazia')
        return v
    
    @validator('idade_cliente')
    def idade_nao_pode_ser_menor_que_dezoito (cls, v):
        if v is not None and v < 18:
            raise ValueError('Idade tem que ser maior que 18 anos')
        return v 


class ClienteCreate(ClienteBase):
    """Schema para CRIAR Cliente"""
    pass


class ClienteUpdate(BaseModel):
    """Schema para ATUALIZAR clientes (todos os campos são opcionais)"""
    nome_cliente: str = Field(..., min_length=1, max_length=100, description="Nome do cliente")
    rg_cliente: float = Field(...,gt=0, description="Digite seu RG")
    cpf_cliente: float = Field(..., gt=0, description="Digite seu CPF")
    endereco_cliente: str = Field(..., min_length=1, max_length=100, description="Endereço")
    telefone_cliente: float = Field(..., gt=0, description="Telefone")
    idade_cliente: float = Field(..., gt=0, description="Data de Nascimento")
    email_cliente: str = Field(..., min_length=1, max_length=100, description="E-mail")
    senha_cliente: SecretStr = Field(..., min_length=6, max_length=100, description="Senha")
   
    @validator('nome_cliente')
    def nome_nao_pode_ser_vazio(cls, v):
        if v is not None and v.strip() == "":
            raise ValueError('Nome não pode ser vazio')
        return v
    
    @validator('email_cliente')
    def email_nao_pode_ser_vazio(cls, v):
        if not v or v.strip() == "":
            raise ValueError('E-mail não pode ser vazio')
        return v.strip()
    
    @validator('senha_cliente')
    def senha_nao_pode_ser_vazio(cls, v):
        texto_senha = v.get_secret_value() if hasattr(v, 'get_secret_value') else v
        if not texto_senha or texto_senha.strip() == "":
            raise ValueError('Senha não pode ser vazia')
        return v
    
    @validator('idade_cliente')
    def idade_nao_pode_ser_menor_que_dezoito (cls, v):
        if v is not None and v < 18:
            raise ValueError('Idade tem que ser maior que 18 anos')
        return v 


class ClienteResponse(ClienteBase):
    """Schema para LER clientes"""
    id_cliente: int
    data_cadastro: datetime
   
    class Config:
        from_attributes = True

# ==================== TABELAS PROFISSIONAIS ====================

class ProfissionalBase(BaseModel):
    """Schema base - campos comuns"""
    nome_profissional: str = Field(..., min_length=1, max_length=100, description="Nome do cliente")
    rg_profissional: float = Field(...,gt=0, description="Digite seu RG")
    cpf_profissional: float = Field(..., gt=0, description="Digite seu CPF")
    endereco_profissional: str = Field(..., min_length=1, max_length=150, description="Endereço")
    telefone_profissional: float = Field(..., gt=0, description="Telefone")
    idade_profissional: int = Field(..., gt=0, description="Data de Nascimento")
    email_profissional: str = Field(..., min_length=1, max_length=100, description="E-mail")
    senha_profissional: SecretStr = Field(..., min_length=6, max_length=100, description="Senha")
        
    @validator('nome_profissional')
    def nome_nao_pode_ser_vazio(cls, v):
        if not v or v.strip() == "":
            raise ValueError('Nome não pode ser vazio')
        return v.strip()
    
    @validator('email_profissional')
    def email_nao_pode_ser_vazio(cls, v):
        if not v or v.strip() == "":
            raise ValueError('E-mail não pode ser vazio')
        return v.strip()
        
    
    @validator('senha_profissional')
    def senha_nao_pode_ser_vazio(cls, v):
        texto_senha = v.get_secret_value() if hasattr(v, 'get_secret_value') else v
        if not texto_senha or texto_senha.strip() == "":
            raise ValueError('Senha não pode ser vazia')
        return v
    
    @validator('idade_profissional')
    def idade_nao_pode_ser_menor_que_dezoito (cls, v):
        if v is not None and v < 18:
            raise ValueError('Idade tem que ser maior que 18 anos')
        return v 


class ProfissionalCreate(ProfissionalBase):
    """Schema para CRIAR Profissional"""
    pass


class ProfissionalUpdate(BaseModel):
    """Schema para ATUALIZAR profissionais (todos os campos são opcionais)"""
    
    nome_profissional: str = Field(..., min_length=1, max_length=100, description="Nome do cliente")
    rg_profissional: float = Field(...,gt=0, description="Digite seu RG")
    cpf_profissional: float = Field(..., gt=0, description="Digite seu CPF")
    endereco_profissional: str = Field(..., min_length=1, max_length=150, description="Endereço")
    telefone_profissional: float = Field(..., gt=0, description="Telefone")
    idade_profissional: int = Field(..., gt=0, description="Data de Nascimento")
    email_profissional: str = Field(..., min_length=1, max_length=100, description="E-mail")
    senha_profissional: str = Field(..., min_length=6, max_length=100, description="Senha")
        
    @validator('nome_profissional')
    def nome_nao_pode_ser_vazio(cls, v):
        if not v or v.strip() == "":
            raise ValueError('Nome não pode ser vazio')
        return v.strip()
    
    @validator('email_profissional')
    def email_nao_pode_ser_vazio(cls, v):
        if not v or v.strip() == "":
            raise ValueError('E-mail não pode ser vazio')
        return v.strip()
        
    
    @validator('senha_profissional')
    def senha_nao_pode_ser_vazio(cls, v):
        texto_senha = v.get_secret_value() if hasattr(v, 'get_secret_value') else v
        if not texto_senha or texto_senha.strip() == "":
            raise ValueError('Senha não pode ser vazia')
        return v
    
    @validator('idade_profissional')
    def idade_nao_pode_ser_menor_que_dezoito (cls, v):
        if v is not None and v < 18:
            raise ValueError('Idade tem que ser maior que 18 anos')
        return v 


class ProfissionalResponse(ProfissionalBase):
    """Schema para LER clientes"""
    id_profissional: int
    data_cadastro: datetime
   
    class Config:
        from_attributes = True
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
import models
import schemas
from database import SessionLocal, engine, Base
from fastapi.staticfiles import StaticFiles

# Criar as tabelas no banco de dados (MySQL / MariaDB)
models.Base.metadata.create_all(bind=engine)

# Criar a aplicação FastAPI
app = FastAPI(
    title="API do Projeto Cuidado Puro",
    description="Sistema completo para controlar clientes e profissionais",
    version="1.0.0"
)

app.mount("/", StaticFiles(directory="static", html=True), name="static")

# ==================== CONFIGURAÇÃO DE CORS ====================
# Permite que o seu front-end (HTML/JS) faça requisições para a API sem bloqueios
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, substitua pelo link do seu site
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependência para obter a sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Schema simples para a rota de Login
class LoginRequest(BaseModel):
    email: str
    senha: str

# ==================== ENDPOINT DE LOGIN (SISTEMA DE PERFIS) ====================
@app.post("/Login", tags=["Autenticação"])
def Login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """Rota unificada de login - Separa Pacientes de Cuidadores automaticamente"""
    
    # 1. Procura primeiro na tabela de Clientes (Pacientes)
    cliente = db.query(models.Cliente).filter(models.Cliente.email_cliente == login_data.email).first()
    if cliente and cliente.senha_cliente == login_data.senha:
        return {
            "status": "sucesso",
            "tipo_usuario": "paciente",
            "nome": cliente.nome_cliente,
            "id": cliente.id_cliente
        }
    
    # 2. Se não achar em Clientes, procura na tabela de Profissionais (Cuidadores)
    profissional = db.query(models.Profissional).filter(models.Profissional.email_profissional == login_data.email).first()
    if profissional and profissional.senha_profissional == login_data.senha:
        return {
            "status": "sucesso",
            "tipo_usuario": "cuidador",
            "nome": profissional.nome_profissional,
            "id": profissional.id_profissional
        }
        
    # 3. Se não encontrar em nenhum ou a senha estiver errada
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="E-mail ou senha incorretos."
    )

# ==================== ENDPOINTS HOME ====================
@app.get("/", tags=["Home"]) 
def home():
    """Página inicial"""
    return {
        "mensagem": "Bem-vindo à API do Cuidado Puro! ",
        "endpoints_disponiveis": {
            "POST /auth/login": "Realizar login por perfil",
            "POST /Clientes": "Cadastrar um novo Cliente/Paciente",
            "POST /Profissionais": "Cadastrar um novo Profissional/Cuidador"
        }
    } 

# ==================== ENDPOINTS CLIENTES ====================
@app.post("/Clientes", tags=["Clientes"], response_model=schemas.ClienteResponse, status_code=201)
def cadastro_cliente(cliente: schemas.ClienteCreate, db: Session = Depends(get_db)):
    """POST - Cadastrar um novo Cliente"""
    # Converte os dados do Pydantic para um dicionário Python simples
    dados_cliente = cliente.model_dump()
    
    # CORREÇÃO: Extrai a string pura da senha do SecretStr antes de mandar para o SQLAlchemy
    dados_cliente["senha_cliente"] = cliente.senha_cliente.get_secret_value()
    
    db_cliente = models.Cliente(**dados_cliente)

    try:
        db.add(db_cliente)
        db.commit()
        db.refresh(db_cliente)
        return db_cliente
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, 
            detail=f"Erro interno ao salvar no banco. Verifique se o e-mail/CPF já existe ou se faltam campos. Detalhe: {str(e)}"
        )

@app.get("/Clientes", tags=["Clientes"], response_model=List[schemas.ClienteResponse])
def listar_clientes(db: Session = Depends(get_db)):
    """GET - Listar todos os Clientes"""
    return db.query(models.Cliente).all()

@app.get("/Clientes/{cliente_id}", tags=["Clientes"], response_model=schemas.ClienteResponse)
def buscar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """GET - Buscar um cliente pelo ID"""
    cliente = db.query(models.Cliente).filter(models.Cliente.id_cliente == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado!")
    return cliente

@app.get("/Clientes/Busca/{nome_cliente}", tags=["Clientes"])
def buscar_por_nome_cliente(nome_cliente: str, db: Session = Depends(get_db)):
    """GET - Buscar clientes pelo nome"""
    clientes = db.query(models.Cliente).filter(
        models.Cliente.nome_cliente.ilike(f"%{nome_cliente}%")
    ).all()
    return clientes

@app.put("/Clientes/{cliente_id}", tags=["Clientes"], response_model=schemas.ClienteResponse)
def atualizar_clientes(cliente_id: int, cliente_update: schemas.ClienteUpdate, db: Session = Depends(get_db)):
    """PUT - Atualizar um cliente existente"""
    cliente = db.query(models.Cliente).filter(models.Cliente.id_cliente == cliente_id).first()
   
    if not cliente:
        raise HTTPException(status_code=404, detail=f"Cliente com ID {cliente_id} não encontrado!")
   
    update_data = cliente_update.model_dump(exclude_unset=True)
   
    for campo, valor in update_data.items():
        setattr(cliente, campo, valor)
   
    db.commit()
    db.refresh(cliente)
    return cliente

@app.delete("/Clientes/{cliente_id}", tags=["Clientes"])
def deletar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """DELETE - Remover um cliente do sistema"""
    cliente = db.query(models.Cliente).filter(models.Cliente.id_cliente == cliente_id).first()
   
    if not cliente:
        raise HTTPException(status_code=404, detail=f"Cliente com ID {cliente_id} não encontrado!")
   
    nome_cliente = cliente.nome_cliente
    db.delete(cliente)
    db.commit()
   
    return {"mensagem": f"Cliente '{nome_cliente}' (ID: {cliente_id}) foi removido com sucesso!"}

# ==================== ENDPOINTS PROFISSIONAL ====================
@app.post("/Profissionais", tags=["Profissionais"], response_model=schemas.ProfissionalResponse, status_code=201)
def cadastro_profissional(profissional: schemas.ProfissionalCreate, db: Session = Depends(get_db)):
    """POST - Cadastrar um novo Profissional"""
    dados_profissional = profissional.model_dump()
    
    # CORREÇÃO: Extrai a string pura da senha do SecretStr
    dados_profissional["senha_profissional"] = profissional.senha_profissional.get_secret_value()
    
    # CORREÇÃO: Alinhado para "models.Profissional" com P maiúsculo conforme convenção padrão
    db_profissional = models.Profissional(**dados_profissional)
    
    try:
        db.add(db_profissional)
        db.commit()
        db.refresh(db_profissional) 
        return db_profissional
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, 
            detail=f"Erro interno ao salvar no banco. Verifique se o e-mail/CPF já existe ou se faltam campos. Detalhe: {str(e)}"
        )

@app.get("/Profissionais", tags=["Profissionais"], response_model=List[schemas.ProfissionalResponse])
def listar_profissionais(db: Session = Depends(get_db)):
    """GET - Listar todos os Profissionais"""
    return db.query(models.Profissional).all()

@app.get("/Profissionais/{profissional_id}", tags=["Profissionais"], response_model=schemas.ProfissionalResponse)
def buscar_profissional(profissional_id: int, db: Session = Depends(get_db)):
    """GET - Buscar um profissional pelo ID"""
    profissional = db.query(models.Profissional).filter(models.Profissional.id_profissional == profissional_id).first()
    if not profissional:
        raise HTTPException(status_code=404, detail="Profissional não encontrado!")
    return profissional

@app.get("/Profissionais/Busca/{nome_profissional}", tags=["Profissionais"])
def buscar_por_nome_profissional(nome_profissional: str, db: Session = Depends(get_db)):
    """GET - Buscar profissionais pelo nome"""
    profissional = db.query(models.Profissional).filter(
        models.Profissional.nome_profissional.ilike(f"%{nome_profissional}%")
    ).all()
    return profissional

@app.put("/Profissionais/{profissional_id}", tags=["Profissionais"], response_model=schemas.ProfissionalResponse)
def atualizar_profissionais(profissional_id: int, profissional_update: schemas.ProfissionalUpdate, db: Session = Depends(get_db)):
    """PUT - Atualizar um profissional existente"""
    profissional = db.query(models.Profissional).filter(models.Profissional.id_profissional == profissional_id).first()
   
    if not profissional:
        raise HTTPException(status_code=404, detail=f"Profissional com ID {profissional_id} não encontrado!")
   
    update_data = profissional_update.model_dump(exclude_unset=True)
   
    for campo, valor in update_data.items():
        setattr(profissional, campo, valor)
   
    db.commit()
    db.refresh(profissional)
    return profissional

@app.delete("/Profissional/{profissional_id}", tags=["Profissionais"])
def deletar_profissional(profissional_id: int, db: Session = Depends(get_db)):
    """DELETE - Remover um profissional do sistema"""
    profissional = db.query(models.Profissional).filter(models.Profissional.id_profissional == profissional_id).first()
    
    if not profissional:
        raise HTTPException(status_code=404, detail=f"Profissional com ID {profissional_id} não encontrado!")
   
    # CORREÇÃO: Alterado de .nome_cliente para .nome_profissional
    nome_profissional = profissional.nome_profissional
    db.delete(profissional)
    db.commit()
   
    return {"mensagem": f"Profissional '{nome_profissional}' (ID: {profissional_id}) foi removido com sucesso!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
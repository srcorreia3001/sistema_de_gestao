from fastapi import FastAPI, Depends, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from . import models

# Cria as tabelas no SQLite local automaticamente se não existirem
Base.metadata.create_all(bind=engine)

app = FastAPI(title="EBD Sistema Escolar - Portfólio")

# Montagem de arquivos estáticos (Tailwind / CSS)
#app.mount("/static", StaticFiles(directory="static"), name="static")

# Configuração dos templates Jinja2
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    turmas = db.query(models.Turma).all()
    alunos = db.query(models.Aluno).all()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "turmas": turmas,
        "alunos": alunos
    })

@app.post("/adicionar-aluno")
def adicionar_aluno(nome: str = Form(...), idade: int = Form(...), tipo: str = Form("Aluno"), turma_id: int = Form(...), db: Session = Depends(get_db)):
    novo_aluno = models.Aluno(nome=nome, idade=idade, tipo=tipo, turma_id=turma_id)
    db.add(novo_aluno)
    db.commit()
    return RedirectResponse(url="/", status_code=303)

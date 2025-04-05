from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import csv
import os
from datetime import datetime
import shutil
from typing import Optional
import uuid

app = FastAPI()

# Configurar CORS para permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas as origens
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos os métodos
    allow_headers=["*"],  # Permitir todos os cabeçalhos
)

# Diretório base para salvar os dados
BASE_DIR = "uploads"

@app.post("/")
async def upload_message(
    nome: str = Form(...),
    relacao: str = Form(...),
    mensagem: Optional[str] = Form(None),
    casal: Optional[str] = Form(None),
    folderPath: Optional[str] = Form(None),
    video: Optional[UploadFile] = File(None)
):
    # Criar o diretório base se não existir
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)
    
    # Determinando o caminho da pasta
    folder_path = folderPath if folderPath else f"videos/{nome.replace(' ', '_')}/"
    full_folder_path = os.path.join(BASE_DIR, folder_path)
    
    # Criar diretório para o usuário se não existir
    if not os.path.exists(full_folder_path):
        os.makedirs(full_folder_path, exist_ok=True)
    
    # Criar diretório de vídeos se não existir
    videos_folder = os.path.join(full_folder_path, "videos")
    if not os.path.exists(videos_folder):
        os.makedirs(videos_folder, exist_ok=True)
    
    # Salvar dados em CSV
    csv_path = os.path.join(full_folder_path, "info.csv")
    
    # Verificar se o arquivo CSV já existe
    file_exists = os.path.isfile(csv_path)
    
    # Formatar a data e hora atual
    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d %H:%M:%S")
    
    # Dados a serem salvos no CSV
    data = {
        "Nome": nome,
        "Relação": relacao,
        "Mensagem": mensagem or "",
        "Casal": casal or "Douglas e Zita",
        "Data de Envio": date_time,
    }
    
    # Adicionar informação do vídeo se enviado
    video_filename = None
    if video:
        # Gerar um nome de arquivo único baseado no nome do usuário e extensão original
        original_extension = os.path.splitext(video.filename)[1] if "." in video.filename else ".mp4"
        safe_filename = f"{nome.replace(' ', '_')}_{uuid.uuid4().hex[:8]}{original_extension}"
        video_filename = safe_filename
        
        # Caminho completo para salvar o vídeo
        video_path = os.path.join(videos_folder, safe_filename)
        
        # Salvar o vídeo
        with open(video_path, "wb") as buffer:
            shutil.copyfileobj(video.file, buffer)
        
        # Adicionar informação do vídeo ao CSV
        data["Vídeo"] = f"videos/{safe_filename}"
    
    # Escrever no arquivo CSV
    with open(csv_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=data.keys())
        
        # Escrever o cabeçalho apenas se o arquivo não existir
        if not file_exists:
            writer.writeheader()
        
        writer.writerow(data)
    
    return {
        "status": "success",
        "message": "Dados salvos com sucesso",
        "data": {
            "folder": folder_path,
            "csv": "info.csv",
            "video": video_filename
        }
    }

# Rota para verificar se a API está online
@app.get("/")
async def read_root():
    return {"status": "online", "message": "API para receber mensagens e vídeos está operacional"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

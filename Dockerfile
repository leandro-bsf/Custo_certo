# 1. Usa uma imagem oficial do Python estável e leve
FROM python:3.11-slim

# 2. Define o diretório de trabalho dentro do container
WORKDIR /app

# 3. Evita que o Python escreva arquivos .pyc no disco e força o output direto no terminal
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 4. Instala dependências do sistema operacional necessárias para compilar pacotes (se houver)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# 5. Copia o arquivo de dependências primeiro (otimiza o cache das camadas do Docker)
COPY requirements.txt .

# 6. Atualiza o pip e instala as dependências da aplicação
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 7. Copia todo o resto do seu código local para dentro do container
COPY . .

# 8. Informa ao Docker que a aplicação escuta na porta padrão do Streamlit
EXPOSE 8501

# 9. Comando para rodar o Streamlit apontando para o seu arquivo principal (ajuste se for main.py)
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
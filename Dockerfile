# Usando uma imagem base do Python
FROM python:3.9-slim

# Instalação de dependências para cfgrib e ecCodes
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libeccodes-dev \
    && rm -rf /var/lib/apt/lists/*

# Diretório de trabalho no contêiner
WORKDIR /app

# Copiar o requirements.txt e instalar as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o script Python para o contêiner
COPY precip_accumulation_v4.py .

# Comando padrão que será executado
ENTRYPOINT ["python", "precip_accumulation_v4.py"]


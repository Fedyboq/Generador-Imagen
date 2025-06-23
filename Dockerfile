FROM ubuntu:22.04

# Configuración para evitar prompts
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-dev \
    build-essential \
    graphviz libgraphviz-dev \
    pkg-config curl unzip git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Crear carpeta de trabajo
WORKDIR /var/task

# Copiar dependencias
COPY app/requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de Lambda
COPY app/lambda_function.py .

# Comando para Lambda (usa lambda_function.handler)
CMD ["lambda_function.handler"]


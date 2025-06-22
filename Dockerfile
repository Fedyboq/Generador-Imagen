FROM amazonlinux:2

# Instalar herramientas básicas
RUN yum update -y && \
    yum groupinstall -y "Development Tools" && \
    yum install -y \
        wget \
        python3 \
        python3-devel \
        cairo-devel \
        libtool \
        libpng-devel \
        libjpeg-devel \
        pango-devel \
        git \
        pkgconfig \
        freetype-devel

# Instalar pip
RUN python3 -m ensurepip && pip3 install --upgrade pip

# Descargar y compilar Graphviz
WORKDIR /opt
RUN wget https://gitlab.com/api/v4/projects/4207231/packages/generic/graphviz-releases/2.49.3/graphviz-2.49.3.tar.gz && \
    tar -xzf graphviz-2.49.3.tar.gz && \
    cd graphviz-2.49.3 && \
    ./configure && \
    make && \
    make install

# Configurar el path para Graphviz
ENV PATH="/usr/local/bin:$PATH"
ENV LD_LIBRARY_PATH="/usr/local/lib:$LD_LIBRARY_PATH"

# Instalar requirements
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copiar código
COPY lambda_function.py .

# Handler para Lambda
CMD ["lambda_function.lambda_handler"]

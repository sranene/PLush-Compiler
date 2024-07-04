# Use a imagem base do Ubuntu 20.04
FROM ubuntu:20.04

# Atualize os pacotes
RUN apt-get update && \
    apt-get install -y llvm clang python3 python3-pip

# Copie os arquivos necessários para o diretório de trabalho do contêiner
WORKDIR /app
COPY main.py /app/
COPY node.py /app/
COPY typechecker.py /app/
COPY compilador.py /app/
COPY plush.sh /app/
COPY functions.c /app/
COPY tests /app/tests

# Instalar dependências
COPY req.txt /app/
RUN pip3 install -r req.txt

# Compilar o código C para LLVM IR
RUN clang -S -emit-llvm -o functions.ll functions.c

# Defina o comando padrão para executar o programa ao iniciar o contêiner
CMD ["python3", "main.py"]

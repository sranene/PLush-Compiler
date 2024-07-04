#!/bin/bash

# Inicializar a flag TREE_FLAG como false
TREE_FLAG=false

# Inicializar um array para armazenar os argumentos sem a flag --tree
ARGS=()

# Verificar cada argumento
for arg in "$@"; do
    if [ "$arg" == "--tree" ]; then
        TREE_FLAG=true
    else
        ARGS+=("$arg")
    fi
done

# Verificar se o arquivo foi especificado
if [ ${#ARGS[@]} -eq 0 ]; then
    echo "Usage: ./plush.sh [--tree] <file>"
    exit 1
fi

# Nome do arquivo de entrada
INPUT_FILE="${ARGS[@]: -1}"

# Executar o compilador Python com ou sem a flag --tree
if $TREE_FLAG; then
    python3 main.py --tree "${ARGS[@]}"
else
    python3 main.py "${ARGS[@]}"
fi

# Verificar se os arquivos LLVM IR foram gerados
if [ -f "code.ll" ] && [ -f "functions.ll" ]; then
    # Compilar code.ll para code.o
    llc -filetype=obj code.ll

    # Compilar functions.ll para functions.o
    llc -filetype=obj functions.ll

    # Nome do executável final é o nome do arquivo de entrada sem a extensão
    EXECUTABLE_NAME=$(basename "${INPUT_FILE}" .pl)

    # Linkar os objetos para gerar o executável final com o nome do arquivo de entrada
    clang -o "$EXECUTABLE_NAME" code.o functions.o
else
    exit 1
fi

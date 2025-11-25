#!/bin/bash

mkdir -p /models

MODEL_URL="https://huggingface.co/TheBloke/Mistral-7B-Instruct-GGUF/resolve/main/mistral-7b-instruct.Q4_K_M.gguf"

echo "Baixando modelo..."
curl -L $MODEL_URL -o /models/model.gguf
echo "Modelo baixado!"

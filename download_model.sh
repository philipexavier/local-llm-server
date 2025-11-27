#!/bin/bash

mkdir -p /models

MODEL_URL="https://huggingface.co/Qwen/Qwen2.5-3B-Instruct-GGUF/resolve/main/qwen2.5-3b-instruct-q4_0.gguf"

echo "Baixando modelo Qwen 2.5 3B Instruct..."
curl -L -H "User-Agent: Mozilla/5.0" "$MODEL_URL" -o /models/model.gguf

echo "Modelo baixado com sucesso!"
ls -lh /models

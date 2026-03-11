#!/bin/bash
set -e

# simplified colab serve script - expects llama.cpp and models folder in current directory
LLAMA_SERVER_PATH="./llama.cpp/build/bin/llama-server"
MODELS_DIR="./models"

MODEL_REPO="unsloth/Qwen3-8B-GGUF"
QUANT_FILE="Qwen3-8B-UD-Q4_K_XL.gguf"

if [ ! -f "$LLAMA_SERVER_PATH" ]; then
    echo "Error: llama-server binary not found at $LLAMA_SERVER_PATH"
    echo "Please run the setup script first: ./setup_llama_cuda.sh"
    exit 1
fi

# Ensure the models directory exists
mkdir -p "$MODELS_DIR"

echo "=========================================="
echo " Serving model: $MODEL_REPO ($QUANT_FILE) with CUDA"
echo " Caching to: $MODELS_DIR"
echo " Thinking mode enabled!"
echo "=========================================="

# Exporting LLAMA_CACHE explicitly forces llama-server to save/read from here
export LLAMA_CACHE="$MODELS_DIR"

# llama-server naturally supports downloading directly from HF using the -hf flag
"$LLAMA_SERVER_PATH" \
    -hf "$MODEL_REPO" \
    --hf-file "$QUANT_FILE" \
    --host 0.0.0.0 \
    --port 8000 \
    --temp 0.6 \
    -c 32768 \
    -b 512 \
    -n 8096 \
    -np 8 \
    -ngl 99 \
    --cache-type-k q8_0 \
    --cache-type-v q8_0 \
    -fa on \
    --chat-template-kwargs '{"enable_thinking":true}'

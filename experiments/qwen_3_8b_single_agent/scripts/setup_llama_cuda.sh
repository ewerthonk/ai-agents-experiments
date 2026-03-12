#!/bin/bash
set -e

# simplified colab setup script - can be run from any directory
LLAMA_CPP_PATH="./llama.cpp"

echo "=========================================="
echo " llama.cpp with CUDA"
echo "=========================================="

# Install system dependencies
echo "=> Installing system dependencies..."
apt-get update
apt-get install pciutils build-essential cmake curl libcurl4-openssl-dev -y

if [ ! -d "$LLAMA_CPP_PATH" ]; then
    echo "=> Cloning llama.cpp..."
    git clone https://github.com/ggml-org/llama.cpp.git "$LLAMA_CPP_PATH"
else
    echo "=> llama.cpp directory already exists. Skipping clone."
fi

echo "=> Building llama.cpp with CUDA support..."
cd "$LLAMA_CPP_PATH"

# Build configuration matching user request
cmake -B build -DBUILD_SHARED_LIBS=OFF -DGGML_CUDA=ON

# Build specific targets
echo "=> Building targets: llama-cli, llama-server,"
cmake --build build --config Release -j --clean-first \
    --target llama-cli \
    --target llama-server

# Copy binaries to root for easier access
echo "=> Copying binaries to $LLAMA_CPP_PATH root..."
cp build/bin/llama-* .

cd ..

echo "=========================================="
echo "=> Setup complete!"
echo "=> Binaries available in $LLAMA_CPP_PATH/"
echo "=========================================="

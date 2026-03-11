#!/bin/bash
set -e

# simplified colab setup script - can be run from any directory
LLAMA_CPP_PATH="./llama.cpp"

echo "=========================================="
echo " llama.cpp with CUDA"
echo "=========================================="

if [ ! -d "$LLAMA_CPP_PATH" ]; then
    echo "=> Cloning llama.cpp..."
    git clone https://github.com/ggml-org/llama.cpp.git "$LLAMA_CPP_PATH"
else
    echo "=> llama.cpp directory already exists. Skipping clone."
fi

echo "=> Building llama.cpp with CUDA support..."
cd "$LLAMA_CPP_PATH"
cmake -B build -DGGML_CUDA=ON
# Only building llama-server and llama-cli exactly as requested to reduce overhead
CMAKE_CORES=$(nproc 2>/dev/null || sysctl -n hw.logicalcpu || echo "2")
cmake --build build --config Release -j $CMAKE_CORES --target llama-server --target llama-cli
cd ..

echo "=> Setup complete! The compiled binaries are ready at $LLAMA_CPP_PATH/build/bin/"

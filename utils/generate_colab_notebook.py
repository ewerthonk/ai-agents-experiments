import os
import json
import argparse
from pathlib import Path

def generate_colab_notebook(experiment_name: str, default_dataset: str = "spider_dev", default_concurrency: int = 5):
    """
    Dynamically generates a Google Colab notebook (.ipynb) for a specific experiment,
    exposing common CLI arguments as Colab variables in the very first cell.
    """
    
    repo_name = "ai_agents"
    github_url = "https://github.com/ewerthonk/ai-agents-experiments.git"
    
    cells = []
    
    def add_markdown(text):
        cells.append({
            "cell_type": "markdown",
            "metadata": {},
            "source": [line + "\n" for line in text.split('\n')]
        })
        
    def add_code(text):
        cells.append({
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [line + "\n" for line in text.split('\n')]
        })

    # --- Setup Notebook Cells ---
    
    add_markdown(f"# Colab Runner: {experiment_name}")
    
    add_markdown("## 0. Configuration Parameters")
    add_code(f"""# The exact name of the dataset zip file mapped in your Google Drive (e.g. 'spider_dev', 'spider_train')
DATASET = "{default_dataset}"

# The name of the experiment (MUST match the exact folder name inside 'experiments/')
EXPERIMENT_NAME = "{experiment_name}"

# Model to be pulled from Hugging Face
MODEL_NAME = "unsloth/Qwen3-8B-GGUF:UD-Q4_K_XL"

# The name of the final prediction text file that will be saved and downloaded
PREDICTION_TXT_FILENAME = "{experiment_name}_colab_run"

# Execute a small sample instead of the full dataset (Requires --sample flag in main.py)
IS_SAMPLE = True

# Concurrency allowed for batch LLM requests
MAX_CONCURRENCY = {default_concurrency}

# Optional tagging tracing purposes
EXPERIMENT_TAG = "{experiment_name}"
""")
    
    add_markdown("## 1. Setup Environment & Clone Repository")
    add_code(f"""# Mount Google Drive to get access to the databases
from google.colab import drive
drive.mount('/content/drive')

# Clone the repository
!git clone {github_url} {repo_name}
%cd {repo_name}

# Copy the dataset from Google Drive and strictly extract it into the spider data path
!mkdir -p data/spider
!cp /content/drive/MyDrive/{{DATASET}}.zip data/spider/
%cd data/spider/
!unzip -q {{DATASET}}.zip
!rm {{DATASET}}.zip
%cd /content/{repo_name}""")

    add_markdown("## 2. Install Dependencies using uv\nWe install `uv` explicitly to resolve `pyproject.toml` extremely fast.")
    add_code("""# Install uv
!pip install uv

# Use uv to install everything from pyproject.toml directly into the colab system env
!uv pip install --system -r pyproject.toml""")

    add_markdown("## 3. Inject API Secrets")
    add_code("""import os
from google.colab import userdata

# Pull the secrets from Colab's native Secret Manager (the little key icon)
os.environ["LANGWATCH_API_KEY"] = userdata.get('LANGWATCH_API_KEY')
os.environ["LANGSMITH_TRACING"] = userdata.get('LANGSMITH_TRACING')
os.environ["LANGSMITH_ENDPOINT"] = userdata.get('LANGSMITH_ENDPOINT')
os.environ["LANGSMITH_API_KEY"] = userdata.get('LANGSMITH_API_KEY')
os.environ["LANGSMITH_PROJECT"] = userdata.get('LANGSMITH_PROJECT')
os.environ["LANGFUSE_SECRET_KEY"] = userdata.get('LANGFUSE_SECRET_KEY')
os.environ["LANGFUSE_PUBLIC_KEY"] = userdata.get('LANGFUSE_PUBLIC_KEY')
os.environ["LANGFUSE_BASE_URL"] = userdata.get('LANGFUSE_BASE_URL')

""")

    add_markdown("## 4. Setup ollama")
    add_code("""!sudo apt update
!sudo apt install -y pciutils zstd
!curl -fsSL https://ollama.com/install.sh | sh""")

    add_markdown("## 5. Serve ollama")
    add_code("""import threading
import subprocess
import time

def run_ollama_serve():
  subprocess.Popen(["ollama", "serve"])

thread = threading.Thread(target=run_ollama_serve)
thread.start()
time.sleep(5)""")

    add_markdown("Pulling ollama model")
    add_code(f"""!ollama pull hf.co/{MODEL_NAME}""")

    add_markdown("## 6. Run the Experiment")
    add_code("""# Ensure sampling string is formatted correctly for bash parsing
SAMPLE_FLAG = "--sample" if IS_SAMPLE else ""

# Run the main pipeline (using -u to force unbuffered logs to the console)
!python -u -m experiments.{EXPERIMENT_NAME}.main \\
    --dataset "{DATASET}" \\
    --prediction_txt_filename "{PREDICTION_TXT_FILENAME}" \\
    --max_concurrency {MAX_CONCURRENCY} \\
    --tag "{EXPERIMENT_TAG}" \\
    {SAMPLE_FLAG}""")

    add_markdown("## 7. Save & Download Results")
    add_code("""import sys
import importlib
from pathlib import Path
from google.colab import files

# Import your own main.py logic dynamically based on whatever EXPERIMENT_NAME is set to in Cell 0!
main_module = importlib.import_module(f"experiments.{EXPERIMENT_NAME}.main")
get_prediction_txt_path = main_module.get_prediction_txt_path

# Determine if main.py used the _sample dataset suffix
actual_dataset = f"{DATASET}_sample" if IS_SAMPLE else DATASET

# Replicate main.py's path resolution exactly
output_file = get_prediction_txt_path(actual_dataset, PREDICTION_TXT_FILENAME)

if output_file.exists():
    print(f"Found prediction file at: {{output_file}}")
    
    # Copy safely to drive
    !cp {{output_file}} /content/drive/MyDrive/
    
    # Trigger browser download
    files.download(str(output_file))
else:
    print(f"Error: Prediction file not found at {{output_file}}! Check the logs above.")""")

    # --- Assemble Notebook ---
    notebook = {
        "cells": cells,
        "metadata": {
            "accelerator": "GPU",
            "colab": {
                "gpuType": "T4",
                "provenance": []
            },
            "kernelspec": {
                "display_name": "Python 3",
                "name": "python3"
            },
            "language_info": {
                "name": "python"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 0
    }

    # --- Save File ---
    experiment_dir = Path(f"experiments/{experiment_name}/colab")
    experiment_dir.mkdir(parents=True, exist_ok=True)
    
    out_path = experiment_dir / f"{experiment_name}_runner.ipynb"
    
    with open(out_path, "w") as f:
        json.dump(notebook, f, indent=1)
        
    print(f"✅ Generated Colab Notebook: {out_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a Colab Notebook for a LangGraph Experiment.")
    parser.add_argument("experiment_name", type=str, help="Name of the experiment folder (e.g. qwen_3_8b_single_agent)")
    parser.add_argument("--dataset", type=str, default="spider_dev", help="Target dataset")
    parser.add_argument("--concurrency", type=int, default=5, help="Max concurrency")
    
    args = parser.parse_args()
    generate_colab_notebook(args.experiment_name, args.dataset, args.concurrency)

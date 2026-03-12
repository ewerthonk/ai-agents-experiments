# Standard Imports
import logging
import argparse
import asyncio
import pandas as pd
import sys
from pathlib import Path

# Project Imports
from settings.settings import settings
from .graph import graph
from .utils.utils import abatch_with_tqdm

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

#Functions
def read_data(dataset: str):
    dataset_path = getattr(settings, f"{dataset}_dataset")
    df = pd.read_parquet(path=dataset_path)
    return df

def get_prediction_txt_path(dataset: str, prediction_txt_filename: str) -> Path:
    """Resolves the exact output path for predictions based on the dataset name."""
    dataset_dir = getattr(settings, f"{dataset}_dir")
    return dataset_dir.joinpath(f"{prediction_txt_filename}.txt")

async def run_graph_in_batch(
    dataset: str = "spider_dev",
    prediction_txt_filename: str = "qwen_3_8b_single_agent",
    max_concurrency: int = 5,
    tag: str = None
):
    df = read_data(dataset)
    prediction_txt_path = get_prediction_txt_path(dataset, prediction_txt_filename)
    inputs = df.assign(dataset=dataset)[["db_id", "question", "dataset"]].to_dict(orient="records")
    
    logger.info(f"Running {prediction_txt_filename} on {len(df)} records with a concurrency of {max_concurrency}")
    config = {
        "max_concurrency": max_concurrency,
        "tags": [tag]
    } if tag else {"max_concurrency": max_concurrency}

    results = await abatch_with_tqdm(graph, inputs, config=config)
    
    df["query"] = [
        result.get("query", "") if isinstance(result, dict) else "" 
        for result in results
    ]

    logger.info(f"Saving predictions to {prediction_txt_path}")
    with open(prediction_txt_path, "w", encoding="utf-8") as file:
        for idx, row in df.iterrows():
            file.write(f"{row['query']}\n")
    logger.info("Batch run complete")


def main():
    parser = argparse.ArgumentParser(description="Run LangGraph Batch.")
    parser.add_argument("--dataset", type=str, default="spider_dev", help="Dataset to use (e.g. 'spider_dev').")
    parser.add_argument("--prediction_txt_filename", type=str, default="qwen_3_8b_single_agent", help="Basename for the txt output.")
    parser.add_argument("--max_concurrency", type=int, default=5, help="Maximum number of concurrent runs.")
    parser.add_argument("--tag", type=str, default=None, help="Tracing tag (e.g. 'experiment 1').")
    parser.add_argument("--sample", action="store_true", help="Run on the sample dataset instead of full.")
    
    args = parser.parse_args()
    
    # Append _sample to dataset if sample flag is used
    actual_dataset = args.dataset
    if args.sample and not actual_dataset.endswith("_sample"):
        actual_dataset = f"{actual_dataset}_sample"

    asyncio.run(run_graph_in_batch(
        dataset=actual_dataset, 
        prediction_txt_filename=args.prediction_txt_filename, 
        max_concurrency=args.max_concurrency, 
        tag=args.tag
    ))


if __name__ == "__main__":
    main()

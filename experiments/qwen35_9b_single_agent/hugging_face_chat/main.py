# Standard Imports
import logging
import argparse
import pandas as pd
import asyncio
import sys
from pathlib import Path
from langchain_core.runnables import RunnableConfig
# from langfuse import get_client
# from langfuse.langchain import CallbackHandler
import langwatch

# Project Imports
from settings.settings import settings
from .graph import graph
from .utils.utils import abatch_with_tqdm

# langwatch.setup()
# langfuse = get_client()
# langfuse_handler = CallbackHandler()

langwatch.setup()

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
    df = pd.read_parquet(path=dataset_path).head(2)
    return df

def get_prediction_txt_path(dataset: str, prediction_txt_filename: str) -> Path:
    """Resolves the exact output path for predictions based on the dataset name."""
    dataset_dir = getattr(settings, f"{dataset}_dir")
    return dataset_dir.joinpath(f"{prediction_txt_filename}.txt")

# async def run_graph_in_batch(
#     dataset: str = "spider_dev",
#     prediction_txt_filename: str = "qwen_3_8b_single_agent",
#     max_concurrency: int = 5,
#     tag: str = None
# ):
#     df = read_data(dataset)
#     prediction_txt_path = get_prediction_txt_path(dataset, prediction_txt_filename)
#     inputs = df.assign(dataset=dataset)[["db_id", "question", "dataset"]].to_dict(orient="records")
    
#     logger.info(f"Running {prediction_txt_filename} on {len(df)} records with a concurrency of {max_concurrency}")
#     config = {
#         "max_concurrency": max_concurrency,
#         "tags": [tag]
#     } if tag else {"max_concurrency": max_concurrency}

#     results = await abatch_with_tqdm(graph, inputs, config=config)
    
#     df["query"] = [
#         result.get("query", "") if isinstance(result, dict) else "" 
#         for result in results
#     ]

#     logger.info(f"Saving predictions to {prediction_txt_path}")
#     with open(prediction_txt_path, "w", encoding="utf-8") as file:
#         for idx, row in df.iterrows():
#             file.write(f"{row['query']}\n")
#     logger.info("Batch run complete")

@langwatch.trace(name="AIAgent")
def run_agent_traced(question: str, db_id: str, dataset: str):
    state_input = {"question": question, "db_id": db_id, "dataset": dataset}
    result = graph.invoke(input=state_input)
    return result.get("query", "") if isinstance(result, dict) else ""

def run_one(input):
    question = input.get("question", "")
    db_id = input.get("db_id", "")
    dataset = input.get("dataset", "")
    
    query = run_agent_traced(question=question, db_id=db_id, dataset=dataset)
    
    result = input.copy()
    result["query"] = query
    return result

def main():
    parser = argparse.ArgumentParser(description="Run LangGraph Batch.")
    parser.add_argument("--dataset", type=str, default="spider_dev", help="Dataset to use (e.g. 'spider_dev').")
    parser.add_argument("--prediction_txt_filename", type=str, default="qwen35_9b_single_agent_hugging_face_chat", help="Basename for the txt output.")
    parser.add_argument("--max_concurrency", type=int, default=4, help="Maximum number of concurrent runs.")
    parser.add_argument("--tag", type=str, default=None, help="Tracing tag (e.g. 'experiment 1').")
    parser.add_argument("--sample", action="store_true", help="Run on the sample dataset instead of full.")
    
    args = parser.parse_args()
    
    # Append _sample to dataset if sample flag is used
    actual_dataset = args.dataset
    if args.sample and not actual_dataset.endswith("_sample"):
        actual_dataset = f"{actual_dataset}_sample"

    # asyncio.run(run_graph_in_batch(
    #     dataset=actual_dataset, 
    #     prediction_txt_filename=args.prediction_txt_filename, 
    #     max_concurrency=args.max_concurrency, 
    #     tag=args.tag
    # ))

    df = read_data(actual_dataset)
    prediction_txt_path = get_prediction_txt_path(actual_dataset, args.prediction_txt_filename)
    inputs = df.assign(dataset=actual_dataset)[["db_id", "question", "dataset"]].to_dict(orient="records")

    results = []
    for input in inputs:
        result = run_one(input)
        results.append(result)
    # results = graph.batch(inputs=inputs,
    #     config=RunnableConfig(
    #         max_concurrency=args.max_concurrency,
    #         tags=[args.tag] if args.tag else None,
    #         # callbacks=[langwatch.get_current_trace().get_langchain_callback(), langfuse_handler]
    #     )
    # )

    df["query"] = [
        result.get("query", "") if isinstance(result, dict) else "" 
        for result in results
    ]

    logger.info(f"Saving predictions to {prediction_txt_path}")
    with open(prediction_txt_path, "w", encoding="utf-8") as file:
        for idx, row in df.iterrows():
            file.write(f"{row['query']}\n")
    logger.info("Batch run complete")


if __name__ == "__main__":
    main()

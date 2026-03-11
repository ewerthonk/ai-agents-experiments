import pandas as pd
from pathlib import Path

def _ingest_json_to_raw_base(
    input_filepath: Path,
    required_columns: list[str],
    gold_filepath: Path | None = None,
) -> pd.DataFrame:
    if not input_filepath.exists():
        raise FileNotFoundError(f"Input file not found: {input_filepath}")

    df = pd.read_json(path_or_buf=input_filepath)

    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"The required column '{col}' was not found in the input JSON.")   

    df = df.loc[:, required_columns]

    if gold_filepath is not None:
        if not gold_filepath.exists():
            raise FileNotFoundError(f"Gold file not found: {gold_filepath}")
        
        with open(gold_filepath, "r", encoding="utf-8") as f:
            gold_lines = [line.strip() for line in f.readlines()]
            
        if len(gold_lines) != len(df):
            raise ValueError(f"Length of gold lines ({len(gold_lines)}) and DataFrame rows ({len(df)}) mismatch.")
            
        df["gold"] = gold_lines

    return df

def _save_raw_parquet(df: pd.DataFrame, output_dir: Path, output_filename: str) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    if not output_filename.endswith(".parquet"):
        output_filename = f"{Path(output_filename).stem}.parquet"
    df.to_parquet(path=output_dir.joinpath(output_filename), index=False)

def ingest_json_to_raw_full(
    input_filepath: Path,
    output_dir: Path,
    output_filename: str = "spider_dev_raw.parquet",
    required_columns: list[str] = ["db_id", "question"],
    gold_filepath: Path | None = None,
) -> pd.DataFrame:
    df = _ingest_json_to_raw_base(input_filepath, required_columns, gold_filepath)
    _save_raw_parquet(df, output_dir, output_filename)
    return df

def ingest_json_to_raw_sample(
    input_filepath: Path,
    output_dir: Path,
    sample_amount: int,
    output_filename: str = "spider_dev_raw_sample.parquet",
    required_columns: list[str] = ["db_id", "question"],
    gold_filepath: Path | None = None,
    random_state: int = 42,
) -> pd.DataFrame:
    df = _ingest_json_to_raw_base(input_filepath, required_columns, gold_filepath)
    
    sample_amount = min(sample_amount, len(df))
    df = df.sample(n=sample_amount, random_state=random_state)
    
    _save_raw_parquet(df, output_dir, output_filename)
    
    if gold_filepath is not None:
        stem = Path(output_filename).stem
        if stem.endswith("_raw_sample"):
            gold_out_filename = stem.replace("_raw_sample", "_gold_sample") + ".txt"
        elif stem.endswith("_raw"):
            gold_out_filename = stem.replace("_raw", "_gold") + ".txt"
        else:
            gold_out_filename = stem + "_gold.txt"
            
        output_dir.mkdir(parents=True, exist_ok=True)
        gold_out_filepath = output_dir.joinpath(gold_out_filename)
        
        with open(gold_out_filepath, "w", encoding="utf-8") as f:
            for gold_query in df["gold"]:
                f.write(f"{gold_query}\n")
        
    return df

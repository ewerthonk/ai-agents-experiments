from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

class Settings(BaseSettings):
    # Folders
    root_dir: Path = Path(__file__).parent.parent.resolve()
    data_dir: Path = root_dir.joinpath("data")

    # Spider
    spider_data_dir: Path = data_dir.joinpath("spider")

    spider_dev_db_dir: Path = spider_data_dir.joinpath("database")
    spider_dev_dir: Path = spider_data_dir.joinpath("spider_dev")
    spider_dev_dataset: Path = spider_dev_dir.joinpath("spider_dev.parquet")
    spider_dev_tables: Path = spider_dev_dir.joinpath("tables.json")
    spider_dev_gold: Path = spider_dev_dir.joinpath("gold.txt")

    spider_dev_sample_db_dir: Path = spider_data_dir.joinpath("database")
    spider_dev_sample_dir: Path = spider_dev_dir.joinpath("sample")
    spider_dev_sample_dataset: Path = spider_dev_sample_dir.joinpath("spider_dev.parquet")
    spider_dev_sample_tables: Path = spider_dev_dir.joinpath("tables.json")
    spider_dev_sample_gold: Path = spider_dev_sample_dir.joinpath("gold.txt")

    spider_test_db_dir: Path = spider_data_dir.joinpath("database")
    spider_test_dir: Path = spider_data_dir.joinpath("test")

    # API Keys
    langwatch_api_key: str | None = None

    # Model Config
    model_config = SettingsConfigDict(
        env_file=root_dir.joinpath("secrets", ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
load_dotenv(settings.model_config["env_file"])
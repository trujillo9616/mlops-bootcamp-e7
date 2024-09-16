import argparse
from typing import Text

import pandas as pd
import yaml

from src.data_preprocess.clean_data import clean_data
from src.utils.logs import get_logger


def data_prepare(config_path: Text) -> None:
    """Load raw data.
    Args:
        config_path {Text}: path to config
    """

    with open(config_path) as conf_file:
        config = yaml.safe_load(conf_file)

    logger = get_logger("DATA_PREPARE", log_level=config["base"]["log_level"])

    logger.info("Loading raw dataset... 🥩")
    df = pd.read_csv(
        config["data_load"]["dataset_csv"], encoding=config["data_load"]["encoding"]
    )

    logger.info("Cleaning data... 🧹")
    df_clean = clean_data(df)

    # Add TotalPrice column
    df_clean["TotalPrice"] = df_clean["UnitPrice"] * df["Quantity"]

    logger.info("Save processed data... 💾")
    df.to_csv(config["data_load"]["dataset_prepare"], index=False)


if __name__ == "__main__":
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument("--config", dest="config", required=True)
    args = args_parser.parse_args()

    data_prepare(config_path=args.config)

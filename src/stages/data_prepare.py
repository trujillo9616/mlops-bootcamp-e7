import argparse
import pandas as pd
from typing import Text
import yaml

from src.utils.logs import get_logger


def data_load(config_path: Text) -> None:
    """Load raw data.
    Args:
        config_path {Text}: path to config
    """

    with open(config_path) as conf_file:
        config = yaml.safe_load(conf_file)

    logger = get_logger('DATA_LOAD', log_level=config['base']['log_level'])

    logger.info('Get dataset')
    # Load the Online Retail dataset
    df = pd.read_csv(config['data_load']['dataset_csv'], encoding=config['data_load']['encoding'])

    #drop duplicates
    logger.info(f"Shape before dropping duplicates {df.shape}")
    df = df.drop_duplicates()
    logger.info(f"Shape after dropping duplicates {df.shape}")

    # drop NaNs
    logger.info(f"Shape before dropping null {df.shape}")
    df = df.dropna(axis=0, how='any')
    logger.info(f"Shape after dropping null {df.shape}")

    # Removing cancelations
    logger.info(f"Shape before dropping negative quantity {df.shape}")
    df[df['Quantity'] < 0]
    logger.info(f"Shape after dropping negative quantity {df.shape}")

    logger.info(f"Shape before dropping negative unit price {df.shape}")
    df = df[df.UnitPrice > 0]
    logger.info(f"Shape after dropping negative unit price {df.shape}")

    logger.info(f"Shape before dropping negative quantity {df.shape}")
    df = df[df.Quantity > 0]
    logger.info(f"Shape after dropping negative quantity {df.shape}")

    # add total sales column
    df['Total_sales'] = df['UnitPrice'] * df['Quantity']

    logger.info('Save processed data')
    df.to_csv(config['data_load']['dataset_prepare'], index=False)


if __name__ == '__main__':

    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('--config', dest='config', required=True)
    args = args_parser.parse_args()

    data_load(config_path=args.config)
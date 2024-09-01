import argparse
import pandas as pd
from typing import Text
import yaml

from src.utils.logs import get_logger

def featurize(config_path: Text) -> None:
    """Create new features.
    Args:
        config_path {Text}: path to config
    """

    with open(config_path) as conf_file:
        config = yaml.safe_load(conf_file)

    logger = get_logger('FEATURIZE', log_level=config['base']['log_level'])

    logger.info('Load prepare data')
    data = pd.read_csv(config['data_load']['dataset_prepare'], encoding=config['data_load']['encoding'])

    logger.info('Calculate Dates')
    # convert date
    data["InvoiceDate"] = pd.to_datetime(data["InvoiceDate"])
    logger.info(f"Minimum Invoice Date {min(data["InvoiceDate"])}")
    logger.info(f"Maximum Invoice Date {max(data["InvoiceDate"])}")

    analysis_date = data["InvoiceDate"].max() + pd.DateOffset(1)
    logger.info(f"RFM Analysis Date : {analysis_date}")

    start_date = analysis_date - pd.DateOffset(days=365)
    logger.info(f"Start Date when taking 1 year data for analysis : {start_date}")

    logger.info('Extract and create features')
    # Aggregate data on a customer level to get RFM values
    data_rfm = data[data.InvoiceDate >= start_date].groupby(['CustomerID'], as_index=False).agg(
        {'InvoiceDate': lambda x: (analysis_date - x.max()).days,
         'InvoiceNo': 'count', 'Total_sales': 'sum'}).rename(columns={'InvoiceDate': 'Recency',
                                                                      'InvoiceNo': 'Frequency',
                                                                      'Total_sales': 'Monetary'})

    ### Getting individual RFM scores by using quantiles for each of the columns
    data_rfm['R_score'] = pd.qcut(data_rfm['Recency'], 4, labels=False)
    data_rfm['F_score'] = pd.qcut(data_rfm['Frequency'], 4, labels=False)
    data_rfm['M_score'] = pd.qcut(data_rfm['Monetary'], 4, labels=False)

    ### Since a low Recency score means recent transactions and good customer, changine quantile values
    ### so that low values rank highest ans vice versa
    data_rfm['R_score'] = 3 - data_rfm['R_score']

    data_rfm['RFM'] = data_rfm.R_score.map(str) \
                      + data_rfm.F_score.map(str) \
                      + data_rfm.M_score.map(str)

    ### Calculating Final RFM score
    data_rfm["RFM_Score"] = data_rfm['R_score'] + data_rfm['F_score'] + data_rfm['M_score']

    logger.info('Save features')
    features_path = config['featurize']['features_path']
    data_rfm.to_csv(features_path, index=False)


if __name__ == '__main__':

    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('--config', dest='config', required=True)
    args = args_parser.parse_args()

    featurize(config_path=args.config)
import argparse
import pandas as pd
from datetime import timedelta
from typing import Text
import yaml
import mlflow

from src.utils.mlflow_run_decorator import mlflow_run
from src.utils.logs import get_logger
from src.rfm.rfm_scoring import (
    recency_scoring,
    frequency_scoring,
    monetary_scoring,
    rfm_scoring,
    categorizer,
)


@mlflow_run
def featurize(config_path: Text) -> None:
    """Create new features.
    Args:
        config_path {Text}: path to config
    """

    with open(config_path) as conf_file:
        config = yaml.safe_load(conf_file)

    logger = get_logger("FEATURIZE", log_level=config["base"]["log_level"])

    logger.info("Load clean data... 💽")
    df = pd.read_csv(
        config["data_load"]["dataset_prepare"], encoding=config["data_load"]["encoding"]
    )

    df.rename(columns=lambda x: x.lower(), inplace=True)

    logger.info("Create new features... 🛠️")
    df["total_price"] = df["quantity"] * df["unitprice"]

    logger.info("Calculate Dates... 📅")

    min_invoice_date, max_invoice_date = min(df["invoicedate"]), max(df["invoicedate"])
    logger.info(f"Minimum Invoice Date: {min_invoice_date}")
    mlflow.log_param("min_invoice_date", min_invoice_date)
    logger.info(f"Maximum Invoice Date: {max_invoice_date}")
    mlflow.log_param("max_invoice_date", max_invoice_date)

    df["last_purchase_date"] = df.groupby("customerid")["invoicedate"].transform("max")
    df["last_purchase_date"] = pd.to_datetime(df["last_purchase_date"]).dt.date

    df["last_purchase_date"] = pd.to_datetime(df["last_purchase_date"])
    df["invoicedate"] = pd.to_datetime(df["invoicedate"])

    df["ref_date"] = df["invoicedate"].max() + timedelta(days=7)
    df["ref_date"] = df["ref_date"].dt.date
    df["ref_date"] = pd.to_datetime(df["ref_date"])

    df["date"] = pd.to_datetime(df["invoicedate"])
    df["date"] = df["date"].dt.date

    ## Calculate Recency
    logger.info("Calculate Recency... 🔄")
    customer_recency = pd.DataFrame(df.groupby("customerid", as_index=False).date.max())

    df["customer_recency"] = df["ref_date"] - df["last_purchase_date"]
    df["recency2"] = pd.to_numeric(df["customer_recency"].dt.days.astype("int64"))

    customer_recency = df.groupby("customerid", as_index=False)["recency2"].mean()
    customer_recency.rename(columns={"recency2": "recency"}, inplace=True)
    df.drop(["last_purchase_date"], axis=1, inplace=True)

    ## Calculate Frequency
    logger.info("Calculate Frequency... 📈")
    customer_frequency = df.groupby("customerid", as_index=False)["invoiceno"].nunique()
    customer_frequency.rename(columns={"invoiceno": "frequency"}, inplace=True)

    ## Calculate Monetary
    logger.info("Calculate Monetary... 💵")
    customer_monetary = df.groupby("customerid", as_index=False)["total_price"].sum()
    customer_monetary.rename(columns={"total_price": "monetary"}, inplace=True)

    ## Merge all the dataframes
    customer_rfm = pd.merge(
        pd.merge(customer_recency, customer_frequency, on="customerid"),
        customer_monetary,
        on="customerid",
    )

    ## Calculate RFM scores
    logger.info("Calculate RFM scores... 🎯")
    customer_rfm["recency_score"] = customer_rfm.apply(recency_scoring, axis=1)
    customer_rfm["frequency_score"] = customer_rfm.apply(frequency_scoring, axis=1)
    customer_rfm["monetary_score"] = customer_rfm.apply(monetary_scoring, axis=1)

    customer_rfm["rfm"] = customer_rfm.apply(rfm_scoring, axis=1)
    customer_rfm["rfm_category"] = customer_rfm["rfm"].apply(categorizer)

    features_path = config["featurize"]["features_path"]
    customer_rfm.to_csv(features_path, index=False)


if __name__ == "__main__":
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument("--config", dest="config", required=True)
    args = args_parser.parse_args()

    featurize(config_path=args.config)

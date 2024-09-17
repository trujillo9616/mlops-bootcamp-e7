import boto3


def upload_results():
    client = boto3.client("s3")
    client.upload_file(
        "data/final/final_online_retail.csv",
        "mlops-bootcamp-datalake",
        "final_online_retail.csv",
    )


if __name__ == "__main__":
    upload_results()

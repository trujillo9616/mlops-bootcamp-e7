import mlflow
import argparse


def start_pipeline(run_name):
    mlflow.set_tracking_uri("https://dagshub.com/trujillo9616/mlops-bootcamp-e7.mlflow")
    mlflow.set_experiment("OnlineRetail")

    with mlflow.start_run(run_name=run_name):
        print(mlflow.active_run().info.run_id)
        mlflow.log_artifact("dvc.yaml")


if __name__ == "__main__":
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument("--run_name", dest="run_name", required=True)
    args = args_parser.parse_args()

    start_pipeline(run_name=args.run_name)

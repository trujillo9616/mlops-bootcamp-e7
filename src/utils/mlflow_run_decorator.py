from functools import wraps
import mlflow


def mlflow_run(wrapped_function):
    @wraps(wrapped_function)
    def wrapper(*args, **kwargs):
        mlflow.set_tracking_uri(
            "https://dagshub.com/trujillo9616/mlops-bootcamp-e7.mlflow"
        )
        mlflow.set_experiment("OnlineRetail")
        with mlflow.start_run():
            return wrapped_function(*args, **kwargs)

    return wrapper

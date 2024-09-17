.PHONY: tests docs

dependencies:
	@echo "Initializing Git..."
	git init
	@echo "Installing dependencies..."
	poetry install
	poetry run pre-commit install

run_pipeline:
	@echo "Running pipeline..."
	export MLFLOW_RUN_ID=`python src/utils/start_pipeline.py --run_name=$(RUN_NAME)`; \
	dvc repro

dependencies_ci:
	@echo "Installing dependencies..."
	poetry install

run_pipeline_ci:
	@echo "Running pipeline..."
	export MLFLOW_RUN_ID=`python src/utils/start_pipeline.py --run_name=`; \
	dvc repro

pull_raw_data:
	@echo "Pulling raw data..."
	dvc pull data/raw/online_retail_raw.csv

env: dependencies
	@echo "Activating virtual environment..."
	poetry shell

tests:
	pytest

docs:
	@echo Save documentation to docs...
	pdoc src -o docs --force
	@echo View API documentation...
	pdoc src --http localhost:8080

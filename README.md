# mlops-bootcamp-e7

Proyecto con implementacion End-to-End de un pipeline de MLOps

By: Adrian Trujillo, Ricardo Diaz

## Project Structure
```bash
.
├── config
│   ├── main.yaml                   # Main configuration file
│   ├── model                       # Configurations for training model
│   └── process                     # Configurations for processing data
├── data
│   ├── final                       # data after training the model
│   ├── processed                   # data after processing
│   ├── raw                         # raw data
│   └── raw.dvc                     # DVC file
├── docs                            # documentation for your project
├── .gitignore                      # ignore files that cannot commit to Git
├── Makefile                        # commands to set up the environment
├── models                          # Models folder
├── notebooks                       # Notebooks folder
├── .pre-commit-config.yaml         # configurations for pre-commit
├── pyproject.toml                  # Poetry dependencies
├── README.md
├── src                             # Main source code
└── tests                           # Tests code
```

### Getting started

**Before you start**

- Get sure you have `python` with a version `>=3.10`, if you want to start from fresh take a look at [this resource](https://wiki.python.org/moin/BeginnersGuide/Download).
- Install `poetry` by following the reccomended instructions in [the oficial documentation](https://python-poetry.org/docs/#installation)

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

To install all the dependencies of this project use

```bash
poetry install
```

To install any other dependency type

```bash
poetry add <package-name>[@<version>]
```

### DVC Data Versioning 💽

DVC (Data Version Control) allows us to version our data, models and other artifacts, without storing them in the git repository (which is not recommended). We will store and track our data to a remote S3 bucket in AWS. To start using DVC as a developer, you have to follow these steps:

1. Install DVC (already installed in the project dependencies with poetry 🎉)

2. Initialize DVC in the project (already done in the project setup 😎)

3. Install AWS CLI and configure it with your credentials. You can follow the instructions in the [official AWS documentation](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html). After you have installed the CLI, you can configure it by running:

```bash
aws configure
```

Your credentials will be stored in `~/.aws/credentials` and `~/.aws/config` files. They will be provided by your AWS administrator.

3. Start using DVC with the following commands:

- To get data from the remote storage:

  ```bash
  dvc pull
  ```

- To add a file to DVC:

  ```bash
  dvc add <file>
  ```

- To commit changes to DVC:

  ```bash
  dvc commit
  ```

- To push changes to the remote storage:

  ```bash
  dvc push
  ```

- To reproduce the data (coming soon with pipelines 🚀):

  ```bash
  dvc repro
  ```

### Pre-commit hooks 🎣

Pre-commit hooks are a set of actions that are executed before a commit is made. They are used to ensure that the code is clean and follows the project's standards. To install the pre-commit hooks, you have to run the following command:

```bash
pre-commit install
```

### Dagshub & MLFlow 🐾🌊

To track the experiments of this repository, we decided to use Dagshub because it offers a MLFlow server that we can send our experiment data and store our models. You can check it out [here](https://dagshub.com/trujillo9616/mlops-bootcamp-e7)

## Contact info

Adrian Trujillo, Ricardo Diaz

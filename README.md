# failed-bank-dataset

This project creates a dataset from the FDIC failed bank list. The dataset is published to kaggle here: [failed-bank-list](https://www.kaggle.com/datasets/ronmallory/failed-bank-list).

## Table of Contents
- [failed-bank-dataset](#failed-bank-dataset)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Pre-Commit Hooks](#pre-commit-hooks)
  - [Publishing Kaggle Dataset](#publishing-kaggle-dataset)
    - [Initial Publish](#initial-publish)
    - [Github action updating dataset.](#github-action-updating-dataset)
  - [Contributing](#contributing)
  - [License](#license)

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/RonMallory/failed-bank-dataset.git
   cd failed-bank-dataset
   ```

2. **Setup with Poetry**:

   Ensure you have [Poetry](https://python-poetry.org/docs/) installed:

   ```bash
   poetry install
   ```

   This command installs all the necessary dependencies specified in `pyproject.toml`.

## Pre-Commit Hooks

This project uses `pre-commit` to maintain code quality and consistency. The following hooks are in place:

```bash
pre-commit install
```

## Publishing Kaggle Dataset

The init dataset is published manually while additional updates to the dataset occur in github actions.

### Initial Publish

1. Create api token from kaggle account settings
2. Run the following command to generate the dataset.csv and the kaggle-metadata.json files
```bash
poetry run python src/main.py
```
3. Run the following command to publish the dataset to kaggle
```bash
kaggle datasets create -p ./data"
```

### Github action updating dataset.

1. With the kaggle.json file that was created in [Initial Publish](#initial-publish) create a github secret with the name KAGGLE_USERNAME and KAGGLE_KEY
2. Once a pull request has been approved and merged into the main branch the github action will run and update the dataset.
   1. The ci.yml file will use the commit message to annotate the dataset with the changes made.

## Contributing

1. Fork the project.
2. Create a branch based on the DSLP strategy: `git checkout -b feature/new-feature`
3. Commit your changes: `git commit -am 'Add new feature'`
4. Push to the branch: `git push origin feature/new-feature`
5. Submit a pull request against the appropriate DSLP branch.

## License

This project is licensed under the MIT License.

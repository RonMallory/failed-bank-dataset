import logging
from fdic_datapipeline import FDICDataPipeline
from get_dataset_metadata import gen_kaggle_metadata
import config

# Get the logging level from the config
logging_level = config.LOGGING_LEVEL.upper()

# Initialize logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(module)s - %(message)s",
    level=logging_level,
)


def main() -> None:
    """Main function to run the data pipeline."""

    # Initialize the data pipeline
    pipeline = FDICDataPipeline(config.FDIC_URL)

    # Define the pipeline configurations
    pipeline_configs = [
        {
            "endpoint": config.FAILURES_ENDPOINT,
            "params": config.FAILURES_PARAMS,
        },
        {
            "endpoint": config.FAILURES_DEFINITION_ENDPOINT,
            "params": {},
        },
    ]

    # Run data collection pipeline
    pipeline.run_data_collection_pipelines(pipeline_configs)

    # Run data Transformation pipeline
    pipeline.run_data_transformation_pipeline()

    # Run dataset-metadata.json generation
    gen_kaggle_metadata()


if __name__ == "__main__":
    main()

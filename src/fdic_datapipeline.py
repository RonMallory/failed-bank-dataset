from file_ops import (
    get_files_in_data_dir,
    clean_data_directory,
    get_data_directory,
)
from api_utils import (
    construct_url,
    download_files,
    download_files_with_pagination,
)
from data_transform import (
    fdic_json_to_csv,
    fdic_yaml_to_csv,
)
import config
import logging
from typing import Dict, List, Optional


class FDICDataPipeline:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.abs_data_dir = get_data_directory(config.DATA_DIR)

        clean_data_directory(self.abs_data_dir)

    def run_data_collection_pipeline(
        self, endpoint: str, params: Dict[str, str]
    ) -> None:
        logging.info(f"Starting Data Pipeline for {endpoint} endpoint.")

        # Cleaning existing data directory

        url = construct_url(self.base_url, endpoint, params)

        if not params:
            logging.info(f"Downloading {endpoint} files.")
            try:
                download_files([url])
            except Exception as e:
                logging.warning(f"Failed to download data with status code {e}")
        elif params["download"] == "true":
            file_name = f"{params['filename']}.{params['format']}"
            logging.info(f"Downloading {file_name} without pagination.")
            download_files([url], file_name)
        elif params["download"] == "false":
            file_name = f"{params['filename']}.{params['format']}"
            logging.info(f"Downloading {file_name} with pagination.")
            download_files_with_pagination(self.base_url, endpoint, params)
        else:
            logging.warning("")

        logging.info(f"Completed Data Pipeline for {endpoint} endpoint.")

    def run_data_collection_pipelines(
        self,
        pipeline_configs: List[Dict[str, Optional[Dict[str, str]]]],
    ) -> None:
        for conf in pipeline_configs:
            endpoint = conf.get("endpoint")
            params = conf.get("params", {})

            if endpoint is None:
                logging.warning("Skipping pipeline due to missing endpoint.")
                continue

            if params is None:
                params = {}

            # Explicitly type-casting to avoid MyPy error
            assert isinstance(endpoint, str)
            assert isinstance(params, dict)

            self.run_data_collection_pipeline(endpoint, params)

    def run_data_transformation_pipeline(self) -> None:
        logging.info("Starting Data Pipeline.")

        logging.info("Transforming JSON files to CSV files.")
        # Get all JSON Files.
        json_files = get_files_in_data_dir(self.abs_data_dir, "json")

        # Transform JSON files to CSV files.
        fdic_json_to_csv(json_files)

        logging.info("Transforming YAML files to CSV files.")
        # Get all YAML Files.
        yaml_files = get_files_in_data_dir(self.abs_data_dir, "yaml")

        # Transform YAML files to CSV files.
        fdic_yaml_to_csv(yaml_files)

        logging.info("Completed Data Pipeline endpoint.")

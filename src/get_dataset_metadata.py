from file_ops import get_data_directory
import logging
import json
import os
import config
import pandas as pd
from typing import Dict, List, Union, Any, cast


class MetadataDiscrepancyError(Exception):
    """Exception raised for discrepancies between metadata and actual files."""

    def __init__(self, message: str) -> None:
        super().__init__(message)


def get_dataset_file_list(data_dir: str = config.DATA_DIR) -> List[str]:
    """
    Get a list of all files in the data/ directory.

    Parameters:
        data_dir (str): The relative or absolute path to the data/ directory.

    Returns:
        List[str]: A list of all files in the data/ directory.
    """
    # Get the absolute path of the data/ directory
    abs_data_dir = get_data_directory(data_dir)

    # Get a list of all files in the data/ directory
    file_list = os.listdir(abs_data_dir)

    # Return the list of files
    return file_list


def compare_resources_with_metadata(
    metadata_dict: Dict[str, Union[str, List[Dict[str, str]]]],
    file_names: List[str],
) -> None:
    """
    Compare resources declared in metadata with actual files.

    Parameters:
    - metadata_dict (Dict): The metadata dictionary.
    - file_names (List[str]): List of file names.

    Raises:
    - MetadataDiscrepancyError: If there are discrepancies between metadata and actual files, or if descriptions are missing. # noqa E501
    """
    resources = metadata_dict.get("resources", [])
    if isinstance(resources, list):
        metadata_resources = {
            resource["path"]: resource.get("description", None)
            for resource in resources
        }
    else:
        metadata_resources = {}

    # Convert list of file names to a set
    directory_files = set(file_names)

    # Find files that are missing in metadata but present in directory
    missing_in_metadata = directory_files - metadata_resources.keys()

    # Find files that are declared in metadata but missing in directory
    missing_in_directory = metadata_resources.keys() - directory_files

    # Check if descriptions are missing for any file paths in metadata
    missing_descriptions = [
        path for path, description in metadata_resources.items() if description is None
    ]

    if missing_in_metadata or missing_in_directory or missing_descriptions:
        error_message = []
        if missing_in_metadata:
            error_message.append(
                f"Files missing in metadata: {', '.join(missing_in_metadata)}"
            )
        if missing_in_directory:
            error_message.append(
                f"Files missing in directory: {', '.join(missing_in_directory)}"
            )
        if missing_descriptions:
            error_message.append(
                f"Missing descriptions for files in metadata: {', '.join(missing_descriptions)}"
            )

        raise MetadataDiscrepancyError("\n".join(error_message))


def create_metadata_file(
    metadata_dict: Dict[str, Union[str, List[Dict[str, str]]]]
) -> None:
    """
    Create the metadata JSON file in the data directory.

    Parameters:
        metadata_dict (Dict): The metadata dictionary to be written to the file.
    """
    # Get the absolute path of the metadata file
    file_name = "dataset-metadata.json"
    output_path = get_data_directory()
    abs_output_file_path = os.path.join(output_path, file_name)

    # Create the directory if it doesn't exist
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Write the metadata to the file
    with open(abs_output_file_path, "w") as f:
        json.dump(metadata_dict, f, indent=4)


def get_failures_column_metadata(metadata_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update the metadata dictionary with column metadata for 'bank_failures.csv'.

    Parameters:
        metadata_dict (Dict): The metadata dictionary.

    Returns:
        Dict: Updated metadata dictionary.

    Raises:
        FileNotFoundError: If 'failure_properties.csv' is not found.
    """
    try:
        data_dir = get_data_directory()
        failures_properties_file = "failure_properties.csv"

        properties_abs_path = os.path.join(data_dir, failures_properties_file)

        properties_df = pd.read_csv(properties_abs_path)

        properties_df.drop(columns=["name"], inplace=True)
        properties_df.rename(columns={"title": "name"}, inplace=True)

        failures_schema = properties_df.to_dict(orient="records")

        resources = cast(List[Dict[str, Any]], metadata_dict.get("resources", []))
        for resource in resources:
            if resource.get("path") == "bank_failures.csv":
                resource["schema"] = resource.get("schema", {})
                resource["schema"]["fields"] = failures_schema
                break
        return metadata_dict
    except FileNotFoundError as e:
        logging.error(f"File not found: {e.filename}")
        return metadata_dict


def gen_kaggle_metadata() -> None:
    """
    Generate the Kaggle dataset metadata JSON file.

    The function performs several steps:
    1. Checks for discrepancies between the metadata and actual files.
    2. Updates the metadata description from a Markdown file.
    3. Updates the metadata schema for 'bank_failures.csv'.

    Raises:
        MetadataDiscrepancyError: If there are discrepancies between metadata and actual files.
    """
    logging.info("Starting kaggle dataset metadata generation")

    # Get the absolute path of the metadata file
    file_name = "dataset-metadata.json"
    output_path = get_data_directory()
    abs_output_file_path = os.path.join(output_path, file_name)

    # Delete the file if it exists
    if os.path.exists(abs_output_file_path):
        os.remove(abs_output_file_path)

    # Get the list of files in the data/ directory
    dataset_files: List[str] = get_dataset_file_list()

    # Load Metadata from config
    meta_data = config.KAGGLE_METADATA

    # Create the directory if it doesn't exist
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Check if metadata and directory files are in sync
    compare_resources_with_metadata(meta_data, dataset_files)
    logging.info("Metadata and directory files are in sync.")

    # generate the metadata.description from markdown file.
    readme_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "METADATA_DESCRIPTION.md",
    )

    with open(readme_path, "r") as file:
        readme = file.read()
    meta_data["description"] = readme

    get_failures_column_metadata(
        metadata_dict=meta_data,
    )

    # Write the metadata to the file
    with open(abs_output_file_path, "w") as f:
        json.dump(meta_data, f, indent=4)

    logging.info("Completed kaggle dataset metadata generation")

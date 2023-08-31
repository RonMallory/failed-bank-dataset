import config
import os
import logging
from typing import List


def clean_data_directory(dir: str) -> None:
    """
    Cleans the data directory by removing all files in the directory.

    Parameters:
        dir (str): The directory to clean.

    Returns:
        None
    """
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Define the destination directory and file path
    destination_dir = os.path.join(script_dir, dir)

    # Create the destination folder if it doesn't exist
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
        logging.info(f"Created directory: {destination_dir}")

    # Remove all files in the directory
    for file in os.listdir(destination_dir):
        file_path = os.path.join(destination_dir, file)
        os.remove(file_path)
        logging.info(f"Removed {file_path}")

    logging.info(f"Successfully cleaned {destination_dir}")


def setup_directory() -> str:
    """
    Set up the destination directory for storing data files.

    This function will create the directory specified in the config.DATA_DIR
    if it doesn't already exist.

    Returns:
        str: The full path of the destination directory.
    """

    # Get the absolute path of the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Combine it with the data directory specified in the config
    destination_dir = os.path.join(script_dir, config.DATA_DIR)

    # Create the directory if it doesn't exist
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
        logging.info(f"Created directory: {destination_dir}")

    return destination_dir


def get_json_files_in_data_dir(data_dir: str) -> List[str]:
    """
    Get a list of all JSON files in the specified data directory.

    Parameters:
        data_dir (str): The path to the directory containing JSON files.

    Returns:
        List[str]: A list of full paths to JSON files in the directory.
    """
    # Get the absolute path of the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Join script directory with the data directory
    abs_data_dir = os.path.join(script_dir, data_dir)

    # List all JSON files in the data directory
    json_files = [
        os.path.join(abs_data_dir, file)
        for file in os.listdir(abs_data_dir)
        if file.endswith(".json")
    ]

    return json_files

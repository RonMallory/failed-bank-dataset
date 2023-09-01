import config
import os
import logging


def get_data_directory(data_dir: str = config.DATA_DIR) -> str:
    """
    Get the data directory specified in the config.

    Parameters:
        data_dir (str): The path relative to the directory containing JSON files.

    Returns:
        str: The full path of the data directory.
    """
    # Get the absolute path of the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Combine it with the data directory specified in the config
    destination_dir = os.path.join(script_dir, config.DATA_DIR)

    return destination_dir


def clean_data_directory(abs_data_dir: str) -> None:
    """
    Cleans the data directory by removing all files in the directory.

    Parameters:
        abs_data_dir (str): The absolute path to the directory containing data files.

    Returns:
        None
    """
    logging.info(f"Cleaning {abs_data_dir} directory.")

    # Create the destination folder if it doesn't exist
    if not os.path.exists(abs_data_dir):
        setup_directory(abs_data_dir)

    # Remove all files in the directory
    for file in os.listdir(abs_data_dir):
        file_path = os.path.join(abs_data_dir, file)
        os.remove(file_path)
        logging.info(f"Removed {os.path.basename(file_path)}")

    logging.info(f"Successfully cleaned {abs_data_dir}")


def setup_directory(abs_data_dir: str) -> str:
    """
    Set up the destination directory for storing data files.

    This function will create the directory specified in the config.DATA_DIR
    if it doesn't already exist.

    Parameters:
        abs_data_dir (str): The absolute path to the directory containing data files.

    Returns:
        str: The full path of the destination directory.
    """

    # Create the directory if it doesn't exist
    if not os.path.exists(abs_data_dir):
        os.makedirs(abs_data_dir)
        logging.info(f"Created directory: {abs_data_dir}")

    return abs_data_dir


def get_files_in_data_dir(abs_data_dir: str, file_extension: str) -> list:
    """
    Returns a list of all files in the data directory with the given file extension.

    Parameters:
        abs_data_dir (str): The absolute path to the data directory.
        file_extension (str): The file extension to filter by (e.g., 'json', 'csv', 'txt').

    Returns:
        list: A list of file paths matching the given extension.
    """

    return [
        os.path.join(abs_data_dir, file)
        for file in os.listdir(abs_data_dir)
        if file.endswith(f".{file_extension}")
    ]

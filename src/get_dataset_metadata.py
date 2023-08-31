import logging
import shutil
import os
import config


def get_dataset_metadata(metadata_file: str) -> None:
    """
    Copies a metadata file from the root directory to the 'data/' directory.

    Parameters:
        metadata_file (str): The relative or absolute path to the metadata file.

    The function checks if the 'data/' directory exists. If not, it creates the directory.
    Then, it copies the metadata file from its current location to the 'data/' directory.
    """
    logging.info("Copying metadata file from root directory to the data/ directory.")

    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Define the destination directory and file path
    destination_dir = os.path.join(script_dir, config.DATA_DIR)
    destination_path = os.path.join(destination_dir, os.path.basename(metadata_file))

    # Create the directory if it doesn't exist
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    # Construct the absolute path of the metadata file
    metadata_file_abs_path = os.path.join(script_dir, metadata_file)

    # Copy the metadata file to the destination directory
    shutil.copyfile(metadata_file_abs_path, destination_path)

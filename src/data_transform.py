import json
import logging
import os
import pandas as pd
from typing import List, Dict


def save_data(
    data: List[Dict], destination_path: str, output_format: str = "json"
) -> None:
    """
    Save a list of dictionaries to a file in the specified format.

    Parameters:
        data (List[Dict]): The data to be saved, as a list of dictionaries.
        destination_path (str): The full path where the file will be saved.
        output_format (str, optional): The format in which to save the data. Currently only supports "json". Default is "json". # noqa E501

    Returns:
        None: The function saves the data to a file in the specified format.

    Raises:
        ValueError: If an unsupported output format is specified.
    """

    if output_format.lower() == "json":
        with open(destination_path, "w") as output_file:
            json.dump(data, output_file)
    else:
        raise ValueError(f"Unsupported output format: {output_format}")


def fdic_json_to_csv(files: List[str]) -> None:
    """
    Convert a list of JSON files to CSV format.

    Parameters:
        files (List[str]): A list of full paths to JSON files to be converted.

    Returns:
        None: The function saves the converted data as CSV files and removes the original JSON files.
    """

    for file_path in files:
        # Log the start of the conversion process for this file
        logging.info(f"Starting conversion of {file_path} to CSV.")

        try:
            # Open and read the JSON file
            with open(file_path, "r") as json_file:
                loaded_json = json.load(json_file)

            # Isolate the 'data' field
            data_field = [item["data"] for item in loaded_json if "data" in item]

            # Normalize just the 'data' field to a flat table
            df = pd.json_normalize(data_field)

            # Save the DataFrame to a CSV file
            csv_file_path = file_path.replace(".json", ".csv")
            df.to_csv(csv_file_path, index=False)

            # Remove the original JSON file
            os.remove(file_path)

            # Log the completion of the conversion process for this file
            logging.info(f"Completed conversion of {file_path} to CSV.")

        except Exception as e:
            # Log any exceptions that occur during the conversion process
            logging.error(f"An error occurred while converting {file_path} to CSV: {e}")

import json
import yaml
import logging
import os
import pandas as pd
from typing import List, Dict, Optional


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
        logging.info(f"Starting conversion of {os.path.basename(file_path)} to CSV.")

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
            logging.info(
                f"Completed conversion of {os.path.basename(file_path)} to CSV."
            )

        except Exception as e:
            # Log any exceptions that occur during the conversion process
            logging.error(
                f"An error occurred while converting {os.path.basename(file_path)} to CSV: {e}"
            )


def fdic_yaml_to_csv(files: List[str]) -> None:
    """
    Converts specific properties in multiple YAML files to individual CSV files.

    This function reads each YAML file in the provided list, navigates to the 'properties'
    section inside the 'data' key, and extracts 'name', 'title', and 'description'
    attributes from each property. It then saves these extracted properties to individual CSV files.

    Parameters:
    - files (List[str]): A list of paths to the YAML files to be read.

    Returns:
    - None: The function saves the extracted data to individual CSV files and returns None.

    Logging:
    - Logs error if any file is not found or YAML parsing fails.
    - Logs info upon successful saving of each CSV file.
    """
    for file_path in files:
        try:
            with open(file_path, "r") as f:
                data = yaml.safe_load(f)
        except FileNotFoundError:
            logging.error(f"File {os.path.basename(file_path)} not found.")
            continue
        except yaml.YAMLError as e:
            logging.error(
                f"Error parsing YAML file at {os.path.basename(file_path)}: {e}"
            )
            continue

        properties_data = (
            data.get("properties", {}).get("data", {}).get("properties", {})
        )
        extracted_properties = []

        for name, attributes in properties_data.items():
            title = attributes.get("title", "N/A")
            description = attributes.get("description", "N/A")
            dtype = str(attributes.get("type", "N/A"))
            extracted_properties.append(
                {
                    "name": name,
                    "title": title,
                    "description": description,
                    "type": dtype,
                }
            )

        try:
            df = pd.DataFrame(extracted_properties)
            csv_path = file_path.replace(".yaml", ".csv")
            df.to_csv(csv_path, index=False)
            logging.info(f"Saved to {os.path.basename(csv_path)}")
            os.remove(file_path)
        except Exception as e:
            logging.error(
                f"Error creating DataFrame or writing to CSV for {file_path}: {e}"
            )


def bank_failures_transformations(
    bank_failures_path: str,
    failure_properties_path: str,
    output_path: Optional[str] = None,
) -> None:
    """
    Transforms the column names of a bank failures CSV file based on a properties CSV file.

    Parameters:
    - bank_failures_path (str): Path to the CSV file containing bank failure data.
    - failure_properties_path (str): Path to the CSV file containing column name mappings.
    - output_path (Optional[str]): Optional path to save the transformed CSV file.
                                   If not provided, the original file will be overwritten.

    Returns:
    None: The function saves the transformed DataFrame to a CSV file.

    Raises:
    - FileNotFoundError: If either of the input CSV files is not found.
    - KeyError: If expected columns are missing in the input DataFrames.
    """
    try:
        # Load both CSV files into Pandas DataFrames
        failures = pd.read_csv(bank_failures_path)
        failures_properties = pd.read_csv(failure_properties_path)

        # Check for required columns
        if "title" not in failures_properties or "name" not in failures_properties:
            raise KeyError(
                "The 'failure_properties' DataFrame must contain 'title' and 'name' columns."
            )

        # Make all values in the title lowercase and replace spaces with underscores
        failures_properties["title"] = (
            failures_properties["title"].str.lower().str.replace(" ", "_")
        )

        # Update the original csv file
        failures_properties.to_csv(failure_properties_path, index=False)

        # Create a mapping dictionary from the 'failure_properties' DataFrame
        column_mapping = dict(
            zip(
                failures_properties["title"],
                failures_properties["name"],
            )
        )

        # Rename the columns in the 'bank_failures' DataFrame
        failures.rename(columns=column_mapping, inplace=True)

        # Save the updated DataFrame to a CSV file
        if output_path:
            failures.to_csv(output_path, index=False)
            logging.info(
                f"Transformed DataFrame saved to {os.path.basename(output_path)}"
            )
        else:
            failures.to_csv(bank_failures_path, index=False)
            logging.info(
                f"Transformed DataFrame saved to {os.path.basename(bank_failures_path)}"
            )

    except FileNotFoundError as e:
        logging.error(f"File not found: {e.filename}")
    except KeyError as e:
        logging.error(f"KeyError: {e}")

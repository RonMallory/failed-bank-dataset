import os
import requests
import logging
from data_transform import save_data
from typing import List, Dict, Union, Optional, Mapping
from file_ops import setup_directory
from urllib.parse import urlencode, urlunparse, urlparse


def construct_url(
    base_url: str,
    api_endpoint: str,
    query_params: Optional[Dict[str, str]] = None,
) -> str:
    """
    Constructs a complete URL given a base URL, an API endpoint, and query parameters.

    Parameters:
    - base_url (str): The base URL (e.g., 'https://www.example.com').
    - api_endpoint (str): The API endpoint or resource path (e.g., '/api/resource').
    - query_params (Optional[Dict[str, str]]): A dictionary containing query parameters as key-value pairs. Defaults to None. # noqa E501

    Returns:
    - str: The complete, encoded URL.

    Example:
    >>> construct_url('https://www.example.com', '/api/resource', {'key': 'value'})
    'https://www.example.com/api/resource?key=value'
    """

    # Parse the base URL to separate the scheme and the netloc
    parsed_base_url = urlparse(base_url)

    # Initialize an empty query string
    query_string = ""

    # Encode the query parameters if they exist
    if query_params:
        query_string = urlencode(query_params)

    # Combine the scheme, netloc, API endpoint, and the encoded query parameters
    full_url = urlunparse(
        (
            parsed_base_url.scheme,
            parsed_base_url.netloc,
            api_endpoint,
            None,
            query_string,
            None,
        )
    )

    return full_url


def make_api_request(
    url: str, params: Mapping[str, Union[str, int]]
) -> Union[None, Dict]:
    """
    Make an API request to the given URL with the specified parameters.

    Parameters:
        url (str): The URL to which the API request will be sent.
        params (Dict[str, Union[str, int]]): The parameters for the API request.

    Returns:
        Union[None, Dict]: The JSON response as a dictionary if the request is successful, otherwise None.

    Logs:
        Various log messages indicating the status and any issues encountered.
    """

    try:
        # Initial API request
        response = requests.get(url, params=params)

        if response.status_code == 200:
            return response.json()

        if response.status_code == 400 and "errors" in response.json():
            error_code = response.json()["errors"][0].get("code", "")
            if error_code == "validate:numericality":
                logging.warning("Setting limit to 500 and retrying")
                mutable_params = dict(params)
                mutable_params["limit"] = str(500)
                requests.get(url, params=mutable_params)
                return None

        # Log warnings for other non-200 status codes
        logging.warning(
            f"Failed to download data with status code {response.status_code}"
        )
        logging.warning(f"The error message is: {response.json()}")
        return None

    except Exception as e:
        # Log any other exceptions
        logging.error(f"An error occurred while downloading data from {url}: {e}")
        return None


def download_files(urls: List[str], output_file_name: Optional[str] = None) -> None:
    """
    Downloads files from a list of URLs and saves them to a specified folder.

    Parameters:
        urls (List[str]): List of URLs to download files from.
        output_file_name (str, optional): Custom file name for the downloaded files. If None, the file name is derived from the URL. # noqa E501

    Returns:
        None
    """

    # Use the setup_directory function to handle directory creation
    destination_dir = setup_directory()

    for url in urls:
        try:
            # Get the file name from the URL
            file_name = output_file_name if output_file_name else url.split("/")[-1]

            # Create the full destination path
            destination_path = os.path.join(destination_dir, file_name)

            # Download and save the file
            response = requests.get(url)
            if response.status_code == 200:
                with open(destination_path, "wb") as f:
                    f.write(response.content)
                logging.info(f"Successfully downloaded {file_name}")
            else:
                logging.warning(
                    f"Failed to download {file_name} with status code {response.status_code}"
                )
        except Exception as e:
            logging.error(f"An error occurred while downloading {url}: {e}")


def download_files_with_pagination(
    base_url: str,
    endpoint: str,
    params: Dict[str, str],
    limit: int = 10000,
    output_format: str = "json",
) -> None:
    offset: int = 0
    all_data: list = []
    params["limit"] = str(limit)
    """
    Download data from an API with pagination support.

    Parameters:
        base_url (str): The base URL for the API.
        endpoint (str): The specific API endpoint for the data.
        params (Dict[str, str]): Parameters to pass in the API request.
        limit (int, optional): The maximum number of records per request. Default is 10,000.
        output_format (str, optional): The format for the saved data file. Default is "json".

    Returns:
        None: The function saves the downloaded data to a file and logs the success.
    """
    offset = 0
    all_data = []
    params["limit"] = str(limit)

    # Setup destination directory and path
    destination_dir = setup_directory()
    file_name = params.get("filename", "default_file_name")
    destination_path = os.path.join(destination_dir, f"{file_name}.{output_format}")

    while True:
        # Update the offset for pagination
        params["offset"] = str(offset)

        # Construct the URL and make the API request
        url = construct_url(base_url, endpoint)
        data = make_api_request(url, params)

        # Check if data is returned and if it contains the "data" key
        if not data or "data" not in data:
            break

        # Add the new data to the list
        all_data.extend(data["data"])

        # Check if this is the last page of data
        if len(data["data"]) < limit:
            break

        # Update the offset for the next page
        offset += limit

    # Save the collected data
    save_data(all_data, destination_path, output_format)

    # Log the success
    logging.info(f"Successfully downloaded all data to {file_name}")

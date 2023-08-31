# This could be "INFO", "DEBUG", "WARNING", "ERROR", or "CRITICAL"
LOGGING_LEVEL = "INFO"

DATA_DIR = "../data"
METADATA_FILE = "./dataset-metadata.json"
FDIC_URL = "https://banks.data.fdic.gov"

FAILURES_ENDPOINT = "/api/failures"
FAILURES_PARAMS = {
    "sort_by": "FAILDATE",
    "sort_order": "DESC",
    "format": "json",
    "download": "false",
    "filename": "bank_failures",
}

LOCATIONS_ENDPOINT = "/api/locations"
LOCATIONS_PARAMS = {
    "format": "json",
    "download": "false",
    "filename": "locations",
}
LOCATIONS_DEFINITION_ENDPOINT = "/docs/locations_definitions.csv"

INSTITUTIONS_ENDPOINT = "/api/institutions"
INSTITUTIONS_PARAMS = {
    "format": "json",
    "download": "false",
    "filename": "institutions",
}
INSTITUTIONS_DEFINITION_ENDPOINT = "/docs/institutions_definitions.csv"
INSTITUTIONS_API_DEFINITIONS = "/docs/institutions_properties.yaml"

FINANCIALS_ENDPOINT = "/api/financials"
FINANCIALS_PARAMS = {
    "format": "json",
    "download": "false",
    "filename": "financials",
}

EVENTS_DEFINITION_ENDPOINT = "/docs/events_definitions.csv"

SOD_ENDPOINT = "/api/sod"
SOD_PARAMS = {
    "format": "json",
    "download": "false",
    "filename": "sod",
}

SUMMARY_ENDPOINT = "/api/summary"
SUMMERY_PARAMS = {
    "sort_by": "YEAR",
    "sort_order": "DESC",
    "format": "json",
    "agg_by": "CERT",
    "agg_term_fields": "YEAR",
    "agg_sum_fields": "ASSET",
    "download": "false",
    "filename": "summary",
}
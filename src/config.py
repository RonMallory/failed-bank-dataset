# This could be "INFO", "DEBUG", "WARNING", "ERROR", or "CRITICAL"
LOGGING_LEVEL = "INFO"

DATA_DIR = "../data"
METADATA_FILE = "./dataset-metadata.json"
KAGGLE_METADATA = {
    "title": "Comprehensive FDIC Public Data on U.S. Bank Institutions and Failures",
    "subtitle": "This data set contains the fdic public data on fdic institutions.",
    "id": "ronmallory/fdic-failed-bank-dataset",
    "licenses": [{"name": "apache-2.0"}],
    "keywords": ["beginner"],
    "annotations": {
        "maintainer": "Ron Mallory",
        "source": "https://banks.data.fdic.gov/api/",
    },
    "resources": [
        {
            "path": "bank_failures.csv",
            "description": "Get detail on historical bank failures from 1934 to present.",
        },
        {
            "path": "events_definitions.csv",
            "description": "CSV definition file for bank events",
        },
        {
            "path": "institutions.csv",
            "description": "Get detail on all FDIC-insured institutions.",
        },
        {
            "path": "institutions_definitions.csv",
            "description": "CSV definition file for bank institutions",
        },
        {
            "path": "locations.csv",
            "description": "Get location details on all FDIC-insured institutions.",
        },
        {
            "path": "locations_definitions.csv",
            "description": "CSV definition file for bank locations",
        },
        {
            "path": "failure_properties.csv",
            "description": "/failures api definitions file converted from yaml to csv.",
        },
    ],
}

FDIC_URL = "https://banks.data.fdic.gov"

FAILURES_ENDPOINT = "/api/failures"
FAILURES_PARAMS = {
    "sort_by": "FAILDATE",
    "sort_order": "DESC",
    "format": "json",
    "download": "false",
    "fields": "NAME,CERT,FIN,CITYST,FAILDATE,FAILYR,SAVR,RESTYPE1,CHCLASS1,RESTYPE,QBFDEP,QBFASSET,COST,PSTALP",
    "filename": "bank_failures",
}
FAILURES_DEFINITION_ENDPOINT = "/docs/failure_properties.yaml"

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

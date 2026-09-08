from datetime import date

from airflow.sdk import Param

DAG_ID = "FORECASTER"

DAG_PARAMS = {
    "encoded_picture": Param(None, type=["null","string"]),
}

DAG_TAGS = ["Forecaster", ]

DAG_DISPLAY_NAME = "Forecaster"

DAG_DESCRIPTION = """
TODO
"""

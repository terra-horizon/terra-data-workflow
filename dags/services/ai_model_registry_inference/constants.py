from datetime import date

from airflow.sdk import Param

DAG_ID = "AI_MODEL_REGISTRY_INFERENCE"

DAG_PARAMS = {
    "encoded_picture": Param(None, type=["null","string"]),
}

DAG_TAGS = ["AiModelRegistryInference", ]

DAG_DISPLAY_NAME = "AI Model Registry Inference"

DAG_DESCRIPTION = """
TODO
"""

from datetime import datetime, timezone

from airflow.sdk import Param

from configurations import ForecasterSubmitterConfig

DAG_ID = "FORECASTER"

DAG_PARAMS = {
    "provider": Param("sentinel-2", type=["string"]),
    "ingestion_profile": Param("forecaster-collector", type=["string"]),
    "submitter_profile": Param("stored-forecast", type=["string"]),
    "aoi_id": Param("sperchios", type=["string"], description="Stable remote-storage identity for the physical AOI."),
    "bbox": Param([22.433493, 38.837552, 22.569555, 38.894223], type=["array"], items={"type": "number"}, minItems=4,
                  maxItems=4, title="Bounding Box",
                  description="[min longitude, min latitude, max longitude, max latitude]"),
    "history_start": Param("2016-01-01", type=["null", "string"], format="date"),
    "target_date": Param(f"{datetime.now(timezone.utc).date()}", type=["null", "string"], format="date"),
    "as_of_date": Param(f"{datetime.now(timezone.utc).date()}", type=["null", "string"], format="date"),
}

DAG_TAGS = ["Forecaster", ]

DAG_DISPLAY_NAME = "Forecaster"

DAG_DESCRIPTION = """
TODO
"""

WAIT_FOR_COMPLETION_POKE_INTERVAL = ForecasterSubmitterConfig().options.poke_interval
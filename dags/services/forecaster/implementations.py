import uuid
from datetime import datetime, timezone
from typing import Any

from configurations import ForecasterDataIngestionConfig, ForecasterSubmitterConfig


def ingestion_builder(access_token: str, dag_context, config: ForecasterDataIngestionConfig) -> tuple[
    str, dict[str, str], dict[str, Any]]:
    payload = {
        "run_job_id": str(uuid.uuid4()),
        "triggered_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "provider": dag_context["params"]["provider"],
        "profile": dag_context["params"]["ingestion_profile"],
        "aoi_id": dag_context["params"]["aoi_id"],
        "bbox": dag_context["params"]["bbox"],
        "run_name": dag_context["params"]["aoi_id"] + datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "history_start": dag_context["params"]["history_start"],
        "target_date": dag_context["params"]["target_date"],
    }
    url: str = config.options.base_url + config.options.endpoints.ingestion_run
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {access_token}",
               "Connection": "keep-alive"}
    return url, headers, payload


def submit_forecast_builder(access_token: str, dag_context, config: ForecasterSubmitterConfig) -> tuple[
    str, dict[str, str], dict[str, str | Any]]:
    payload = {
        "run_job_id": str(uuid.uuid4()),
        "triggered_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "profile": dag_context["params"]["submitter_profile"],
        "aoi_id": dag_context["params"]["aoi_id"],
        "run_name": dag_context["params"]["aoi_id"] + datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "as_of_date": dag_context["params"]["as_of_date"]
    }
    url: str = config.options.base_url + config.options.endpoints.submit_job
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {access_token}",
               "Connection": "keep-alive", "X-API-Key": config.options.x_api_key}
    return url, headers, payload


def wait_for_completion_builder(access_token: str, dag_context, config: ForecasterSubmitterConfig, job_id: str):
    url: str = config.options.base_url + config.options.endpoints.ask_status.format(job_id=job_id)
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {access_token}",
               "Connection": "keep-alive", "X-API-Key": config.options.x_api_key}
    return url, headers

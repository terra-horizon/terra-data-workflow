import pendulum
from airflow.exceptions import AirflowFailException
from airflow.sdk import dag, task, get_current_context

from authorization.forecaster_data_ingestion_auth import ForecasterDataIngestionAuthService
from authorization.forecaster_submitter_auth import ForecasterSubmitterAuthService
from common.enum import ForecasterSubmitterJobStatus
from common.extensions.callbacks import on_execute_callback, on_retry_callback, on_failure_callback, \
    on_success_callback, on_skipped_callback
from common.extensions.http_requests import http_post_unsafe, http_get_unsafe
from configurations import ForecasterDataIngestionConfig, ForecasterSubmitterConfig
from services.forecaster import DAG_ID, DAG_TAGS, DAG_DISPLAY_NAME, DAG_DESCRIPTION, DAG_PARAMS, ingestion_builder, \
    WAIT_FOR_COMPLETION_POKE_INTERVAL, submit_forecast_builder, wait_for_completion_builder
from services.logging import Logger


@dag(DAG_ID, tags=DAG_TAGS, dag_display_name=DAG_DISPLAY_NAME, description=DAG_DESCRIPTION, params=DAG_PARAMS,
     schedule="0 0 * * *", start_date=pendulum.datetime(2026, 9, 8, tz="UTC"))
def forecaster():
    forecaster_data_ingestion_config = ForecasterDataIngestionConfig()
    forecaster_submitter_config = ForecasterSubmitterConfig()
    forecaster_data_ingestion_auth = ForecasterDataIngestionAuthService()
    forecaster_submitter_auth = ForecasterSubmitterAuthService()

    @task(on_execute_callback=on_execute_callback, on_retry_callback=on_retry_callback,
          on_success_callback=on_success_callback, on_failure_callback=on_failure_callback,
          on_skipped_callback=on_skipped_callback)
    def run_ingestion():
        log = Logger()
        dag_context = get_current_context()
        # url, headers, payload = ingestion_builder(forecaster_data_ingestion_auth.get_token(), dag_context, forecaster_data_ingestion_config)
        url, headers, payload = ingestion_builder("", dag_context, forecaster_data_ingestion_config)
        log.info_payload("payload", payload, True)
        response = http_post_unsafe(url=url, headers=headers,
                                    data=payload)  # TODO: when the endpoint is protected by SSL, remove the unsafe option
        log.info_payload("server response", response, True)
        return response

    @task(on_execute_callback=on_execute_callback, on_retry_callback=on_retry_callback,
          on_success_callback=on_success_callback, on_failure_callback=on_failure_callback,
          on_skipped_callback=on_skipped_callback)
    def submit_forecast_job():
        log = Logger()
        dag_context = get_current_context()
        url, headers, payload = submit_forecast_builder("", dag_context, forecaster_submitter_config)
        response = http_post_unsafe(url=url, headers=headers, data=payload)
        log.info_payload("server response", response, True)
        return response["job_id"]

    @task.sensor(on_execute_callback=on_execute_callback, on_retry_callback=on_retry_callback,
                 on_success_callback=on_success_callback, on_failure_callback=on_failure_callback,
                 on_skipped_callback=on_skipped_callback, poke_interval=WAIT_FOR_COMPLETION_POKE_INTERVAL,
                 mode="reschedule")
    def wait_for_completion(job_id: str):
        log = Logger()
        dag_context = get_current_context()
        url, headers = wait_for_completion_builder("", dag_context, forecaster_submitter_config, job_id)
        response = http_get_unsafe(url=url, headers=headers)
        log.info_payload("server response", response, True)
        status = ForecasterSubmitterJobStatus(response["status"])
        if status is ForecasterSubmitterJobStatus.FAILED:
            error_message = f"Job id {job_id} has failed"
            log.error(error_message)
            raise AirflowFailException(error_message)
        else:
            log.info_payload(f"Job id {job_id} status", status)
        return status is ForecasterSubmitterJobStatus.SUCCEEDED

    run_ingestion_response = run_ingestion()
    submit_forecast_job_response = submit_forecast_job()
    _ = wait_for_completion(submit_forecast_job_response)

    run_ingestion_response >> submit_forecast_job_response


forecaster()

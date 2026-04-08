from airflow.sdk import task, dag, get_current_context

from authorization.ai_model_registry_auth import AiModelRegistryAuthService
from common.extensions.callbacks import on_execute_callback, on_retry_callback, on_success_callback, \
    on_failure_callback, on_skipped_callback
from common.extensions.http_requests import http_post
from configurations import AiModelRegistryConfig
from services.ai_model_registry_inference import DAG_ID, DAG_TAGS, DAG_DISPLAY_NAME, DAG_DESCRIPTION, DAG_PARAMS, \
    infer_builder
from services.logging import Logger


@dag(DAG_ID, tags=DAG_TAGS, dag_display_name=DAG_DISPLAY_NAME, description=DAG_DESCRIPTION, params=DAG_PARAMS)
def ai_model_registry_inference():
    ai_model_registry_config = AiModelRegistryConfig()
    ai_model_registry_auth = AiModelRegistryAuthService()

    @task(on_execute_callback=on_execute_callback, on_retry_callback=on_retry_callback,
          on_success_callback=on_success_callback, on_failure_callback=on_failure_callback,
          on_skipped_callback=on_skipped_callback)
    def infer():
        log = Logger()
        dag_context = get_current_context()
        url, headers, payload = infer_builder(ai_model_registry_auth.get_token(), dag_context, ai_model_registry_config)
        log.info(f"Payload:\n{payload}\n")
        response = http_post(url=url, headers=headers, data=payload)
        log.info(f"\n{response}\n")
        return response

    _ = infer()


ai_model_registry_inference()

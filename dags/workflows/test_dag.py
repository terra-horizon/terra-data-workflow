from airflow.sdk import task, dag, Param, get_current_context

from services.logging import Logger
from common.extensions.callbacks import on_execute_callback, on_retry_callback, on_success_callback, \
    on_failure_callback, on_skipped_callback


@dag("TEST", tags=["TEST"], dag_display_name="Test", description="foo", params={})
def test():
    @task(on_execute_callback=on_execute_callback, on_retry_callback=on_retry_callback,
          on_success_callback=on_success_callback, on_failure_callback=on_failure_callback,
          on_skipped_callback=on_skipped_callback)
    def test_1():
        log = Logger()
        log.info("Hippity Hoppety hop")
        return True

    _ = test_1()


test()

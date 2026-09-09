from airflow.sdk import Context

from services.logging import Logger
import json

def on_execute_callback(context: Context) -> None:
    log = Logger(context)
    log.info_payload("on_execute", context, False)


def on_retry_callback(context: Context) -> None:
    log = Logger(context)
    log.info_payload("on_retry", context, False)


def on_success_callback(context: Context) -> None:
    log = Logger(context)
    log.info_payload("on_success", context, False)


def on_failure_callback(context: Context) -> None:
    log = Logger(context)
    log.info_payload("on_failure", context, False)


def on_skipped_callback(context: Context) -> None:
    log = Logger(context)
    log.info_payload("on_skipped", context, False)

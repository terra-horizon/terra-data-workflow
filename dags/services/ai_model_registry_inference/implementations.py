from typing import Any

from configurations import AiModelRegistryConfig


def infer_builder(access_token: str, dag_context, config: AiModelRegistryConfig) -> tuple[
    str, dict[str, str], dict[str, Any]]:
    payload = {"encoded_picture": dag_context["params"]["encoded_picture"]}
    url: str = config.options.base_url + config.options.endpoints.infer
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {access_token}",
               "Connection": "keep-alive"}
    return url, headers, payload

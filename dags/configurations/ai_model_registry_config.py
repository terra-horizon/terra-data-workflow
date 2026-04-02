from airflow.sdk import Variable

from configurations.base_config import BaseConfig


class AiModelRegistryConfig:
    class AiModelRegistryCoreConfig:
        class EndpointsConfig:
            def __init__(self, data: dict):
                self.infer = data["infer"]

        def __init__(self, data: dict):
            self.base_url = data.get("base_url")
            self.scope = data.get("scope")
            self.endpoints = self.EndpointsConfig(data.get("endpoints"))

    def __init__(self):
        self.login_client_id = Variable.get("aai_clientid")
        self.login_client_password = Variable.get("aai_clientsecret")
        aai_core = BaseConfig(Variable.get("aai", deserialize_json=True))
        self.login_url = aai_core.base_url
        self.options = self.AiModelRegistryCoreConfig(Variable.get("ai_model_registry", deserialize_json=True))



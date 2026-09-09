from airflow.sdk import Variable

from configurations.base_config import BaseConfig


class ForecasterSubmitterConfig:
    class ForecasterSubmitterCoreConfig:
        class EndpointsConfig:
            def __init__(self, data: dict):
                self.submit_job = data["submit_job"]
                self.ask_status = data["ask_status"]

        def __init__(self, data: dict):
            self.base_url = data.get("base_url")
            self.scope = data.get("scope")
            self.poke_interval = data.get("poke_interval")
            self.x_api_key = data.get("x_api_key")
            self.endpoints = self.EndpointsConfig(data.get("endpoints"))

    def __init__(self):
        self.login_client_id = Variable.get("aai_clientid")
        self.login_client_password = Variable.get("aai_clientsecret")
        aai_core = BaseConfig(Variable.get("aai", deserialize_json=True))
        self.login_url = aai_core.base_url
        self.options = self.ForecasterSubmitterCoreConfig(Variable.get("forecaster_submitter", deserialize_json=True))



from obproject import ProjectFlow
from metaflow import step, pypi, secrets, Config, FlowSpec

class LiteLLMProxyBatchDemo(FlowSpec):

    config = Config("config", default="config.json")

    @secrets(sources=config.secrets)
    @pypi(packages={"openai": ""})
    @step
    def start(self):
        import os
        from openai import OpenAI # pylint: disable=import-error
        from metaflow.metaflow_config import SERVICE_HEADERS

        client = OpenAI(
            api_key="dummy",
            base_url=os.getenv("LITELLM_PROXY_URL")
        )

        self.responses = []
        for model in self.config.models: 
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": "Hello, how are you?"
                    }
                ],
                extra_headers = SERVICE_HEADERS
            )
            self.responses.append(response)
        self.next(self.end)

    @step
    def end(self):
        pass

if __name__ == "__main__":
    LiteLLMProxyBatchDemo()
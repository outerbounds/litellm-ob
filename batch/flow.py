from metaflow import FlowSpec, step, pypi, secrets, Config, config_expr

class LiteLLMBatchDemo(FlowSpec):

    config = Config("config", default="config.json")

    @secrets(sources=config.secrets)
    @pypi(packages={"litellm": ""})
    @step
    @step
    def start(self):
        import litellm
        import os

        # NOTE: If you do not use the standard API KEY name
        # in the Outerbounds Integration that feeds @secrets,
        # you can use this handy feature to set it in LiteLLM.
        # For example, here we have set openai_api env var in 
        # the Outerbounds integration instead of the standard
        # OPENAI_API_KEY. No problem! Of course, you can also
        # set OPENAI_API_KEY in the Outerbounds integration
        # and you will not need to do this. That is what this
        # example does with ANTHROPIC_API_KEY.
        litellm.openai_key = os.environ["openai_api"]

        self.responses = []
        for model in self.config.models: 
            # A trivial loop over each model we want to test.
            # Notice that we'll need to match the API keys 
            # provided in the Outerbounds Integration with the
            # models we aim to test.
            response = litellm.completion(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": "Hello, how are you?"
                    }
                ]
            )
            self.responses.append(response)
        self.next(self.end)

    @step
    def end(self):
        pass

if __name__ == "__main__":
    LiteLLMBatchDemo()
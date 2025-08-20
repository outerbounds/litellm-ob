import os
from metaflow import (
    FlowSpec,
    step,
    current,
    IncludeFile,
    kubernetes,
    environment,
    huggingface_hub,
    secrets,
    Parameter
)
from obproject import ProjectFlow

def model_cache_environment(func):
    deco_list = [
        huggingface_hub(temp_dir_root="metaflow-chkpt/hf_hub"),
        environment(
            vars={
                "HF_HUB_ENABLE_HF_TRANSFER": "1",  
                # Enable Hugging Face transfer acceleration
            }
        ),
        secrets(sources=["outerbounds.eddie-hf"]),
        kubernetes(
            compute_pool="litellm-proxy",
            use_tmpfs=True,
            image='docker.io/eddieob/hf-model-cache'
        )
    ]
    for deco in deco_list:
        func = deco(func)
    return func

class ModelCacher(FlowSpec):

    config = IncludeFile(
        "config",
        default=os.path.join(os.path.dirname(__file__), "config.yaml"),
        is_text=True,
    )

    prev_model_key = Parameter(
        "pre-model-key", 
        default=None,
        type=str
    )
    
    @step
    def start(self):
        self.next(self.pull_model)

    @model_cache_environment
    @step
    def pull_model(self):
        '''
        Cache the model weights in Metaflow datastore.
        Downstream use cases:
            - @model
            - load_model on inference server
        '''
        import yaml
        from omegaconf import OmegaConf # pylint: disable=import-error

        config = OmegaConf.create(yaml.safe_load(self.config))
        config = OmegaConf.to_container(config, resolve=True)
        self.model_name = config["huggingface"]["repo_id"]
        current.run.add_tag("model:%s" % self.model_name)

        print(f"Prev model key: {self.prev_model_key}")
        if self.prev_model_key is None or self.prev_model_key == "null" or self.prev_model_key == "":
            print("Downloading base model")
            self.base_model = current.huggingface_hub.snapshot_download(
                repo_id=self.model_name,
                allow_patterns=config["huggingface"]["allow_patterns"],
                max_workers=100,
                repo_type="model",
            )
        else: 
            print("Using previous model")
            self.base_model = self.prev_model_key
        print(f"Base model: {self.base_model}")
        self.next(self.end)

    @step
    def end(self):
        pass


if __name__ == "__main__":
    ModelCacher()
import argparse
from metaflow import load_model, Flow, namespace

def download_model(local_model_dir, flow_name="ModelCacher"):
    '''
    Executre the model download policy.
    This minimal example uses the most latest run from the upstream flow.

    The base_model artifact is derived from the ModelCacher flow implementation.
    '''
    namespace(None)
    flow = Flow(flow_name)  
    latest_successful_run = flow.latest_successful_run
    model_ref = latest_successful_run.data.base_model
    load_model(model_ref, local_model_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_dir", type=str, required=True)
    parser.add_argument("--flow_name", type=str, required=True)
    args = parser.parse_args()
    download_model(args.model_dir, args.flow_name)
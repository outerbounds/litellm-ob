## Running LiteLLM on Outerbounds

[LiteLLM](https://docs.litellm.ai/docs/) has two components that can be used with Outerbounds.
1. The [Python SDK](https://docs.litellm.ai/docs/#basic-usage) 
2. The [Proxy Server](https://docs.litellm.ai/docs/simple_proxy)

## Use case 1: Batch inference

The eventual goal is to run this workflow, which is a minimal example from which you can build batch inference pipelines.
Follow the two-step setup plan within this section before running this command.

```bash
cd batch
python flow.py --environment=fast-bakery run --with kubernetes
```

### Step 1: Set up Outerbounds integrations for each LLM provider you want to leverage

One of the main functions of LiteLLM is to unify interfaces across LLM providers. 
Providers typically require API keys. For example, to use LiteLLM's OpenAI integration, 
you need to set the `OPENAI_API_KEY` environment variable. Please read [here](https://docs.litellm.ai/docs/set_keys) for more details.

As a one time setup step on Outerbounds, you should visit the `Integrations` tab in Outerbounds UI, 
where you can register provider API keys as secrets by clicking `Add New Integration`.
This makes the secret keys and values accessible in a secure manner in your Outerbounds environments such as workstations, inference servers, and workflow tasks.

### Step 2: Run a workflow using LiteLLM Python client

In `flow.py`, you will find a sample workflow that uses these components to call the LiteLLM client from a Metaflow task:
1. Leverage the secret created in step 1 to authenticate to LLM providers
2. Install LiteLLM using Metaflow's `@pypi` decorator

Running the flow will use LiteLLM from the runtime of the Metaflow task. 

## Use case 2: Real-time inference (LiteLLM proxy server)

```bash
cd realtime
outerbounds app deploy --config-file app_config.yaml
```

### Step 1: Set up Outerbounds integration (or reuse from use case 1)

See Step 1 from the batch inference section, the same Outerbounds Integrations functionality is reused in the `realtime/app_config.yaml` specification.
If you already configured your integrations, you can simply reuse them. 

### Step 2: Deploy and endpoint for the LiteLLM proxy server as an Outerbounds Deployment

After running the `outerbounds app deploy ...` command, you'll see output such as:

```bash
2025-08-13 15:45:04.520 🚀 Deploying litellm-proxy to the Outerbounds platform...
2025-08-13 15:45:04.521 📦 Packaging directory : /path/to/working-dir/litellm-ob/realtime
2025-08-13 15:45:04.522 🐳 Using the docker image : ghcr.io/berriai/litellm:main-latest
2025-08-13 15:45:05.320 💾 Code package saved to : s3://obp-**-metaflow/metaflow/mf.obp-apps/**/**
2025-08-13 15:45:05.451 🚀 Deploying endpoint to the platform....                                   
2025-08-13 15:45:09.504 ⏳ 1 new worker(s) pending. Total pending (1)to serve traffic ⠏
2025-08-13 15:45:31.294 🚀 1 worker(s) started running. Total running (1)erve traffic ⠏
2025-08-13 15:45:31.294 ✅ First worker came online
2025-08-13 15:45:31.294 🎉 All workers are now running
2025-08-13 15:46:16.922 💊 Endpoint deployment status: completed ady to serve traffic ⠼
2025-08-13 15:46:16.922 💊 Running last minute readiness check for **...
2025-08-13 15:46:21.496 💊 Endpoint ** is ready to serve traffic on the URL: https://api-**.**.outerbounds.xyz
2025-08-13 15:46:21.510 💊 Endpoint litellm-proxy (**) deployed! Endpoint available on the URL: https://api-**.**.outerbounds.xyz
```

The key thing to extract is the URL, which contains an HTTP endpoint that you can send
requests to from any machine with your Outerbounds user credentials, 
or machine user credentials in CI environments,
to authorize access when making requests to the LiteLLM endpoint.
Select this value and store in the environment where you want to make client-side requests from,
using the environment variable `LITELLM_PROXY_URL`. 

### Step 3: Access the endpoint

Now you have a full-fledged LiteLLM server. 
You can query it using CURL or from a Python script, anywhere where your Outerbounds user or a machine user is authenticated.
After setting `LITELLM_PROXY_URL` from such an environment, you can run a client-side test with
```bash
cd realtime
python client_sample.py
```

## Extensions 

Most LiteLLM integrations should extend naturally from these two interaction mode templates. 
If you need custom support, or have general question, please reach out in your dedicate Outerbounds Slack channel.
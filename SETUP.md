# Laya setup guide

This repository runs Laya's English decision checkpoint with a Gradio playground
and a named `/systemone` API. It answers typed questions and returns probabilities;
it does not generate code or provide an OpenAI/Ollama chat endpoint.

## Try the public demo

Open [VedantAndhale/laya](https://huggingface.co/spaces/VedantAndhale/laya),
enter your state and questions, and click **Decide**.
You can also call its API from your app using the example below.

The model downloads automatically when the Space starts. There is no separate
Ollama installation, model server, or database to attach.

## Duplicate the public Space

This is the quickest way to create your own deployment:

1. Open [VedantAndhale/laya](https://huggingface.co/spaces/VedantAndhale/laya).
2. Open the Space's three-dot menu and select **Duplicate this Space**.
3. Choose your account and a new Space name, and set visibility to **Public**.
4. Select **ZeroGPU** hardware if your account is eligible. Duplicates may default
   to CPU Basic; this app explicitly loads on CUDA and needs ZeroGPU or a supported GPU.
5. Create the duplicate and wait for its status to become **Running**.
6. Test **Decide**, then use your own Space name in the API client below.

Your duplicate has its own repository and hardware settings. Requests to it are
subject to Hugging Face's GPU allocation and caller usage quotas. It does not
automatically follow later changes to the original Space.

## Customize with the GitHub template

1. Open [Use this template](https://github.com/VedantAndhale/laya/generate).
2. Create a new public repository under your account.
3. Clone your new repository and edit the example questions, title, or model variable.
4. Deploy those files to your own Space using the steps below.

You can also fork the repository if you want a GitHub fork linked to this project.
GitHub templates and forks do not create a Hugging Face deployment automatically.

## Deploy from your repository

1. Create a Space with the **Gradio** SDK and a blank template.
2. Select **ZeroGPU** hardware if your account is eligible. This app is configured
   for CUDA; selecting CPU Basic alone does not turn it into a CPU deployment.
3. Upload `app.py`, `requirements.txt`, and `README.md` from this repository.
   Keep the YAML configuration at the top of `README.md`.
4. Wait for the build and model download to finish. When the status is **Running**,
   test the default refund example. The expected team is `billing`.
5. Open **Use via API** on the app for its generated API instructions.

You can upload through the Space's **Files** tab, or use the Hugging Face CLI:

```sh
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
python -m pip install --upgrade huggingface_hub
hf auth login
hf upload YOUR_USERNAME/YOUR_SPACE . --type space --include app.py --include requirements.txt --include README.md --include SETUP.md
```

Use a token with write access to the destination Space for uploading. Enter it
at the login prompt rather than putting it in source files or command arguments.

The optional `LAYA_MODEL` variable in **Settings → Variables and secrets** selects
another compatible Laya checkpoint. The default is `convaiinnovations/laya`.

## Call the public API from any app or Space

The calling Space does not need Laya, PyTorch, or the model weights installed.
Add this line to its own `requirements.txt`:

```text
gradio_client>=2.7.2
```

No token is required for the public API example. The calling app can run on your
computer, a public Hugging Face Space, or another hosting service.

Use this in the calling app's Python code:

```python
import json
from gradio_client import Client

client = Client("VedantAndhale/laya")

def classify_request(message):
    questions = {
        "team": {
            "type": "choice",
            "instructions": "Which team should handle this request?",
            "criteria": {
                "billing": "payments, duplicate charges and refunds",
                "technical": "software bugs and technical issues",
                "general": "other questions",
            },
        }
    }
    return client.predict(
        state=message,
        questions=json.dumps(questions),
        api_name="/systemone",
    )

result = classify_request("I was charged twice and want a refund.")
print(result["answers"]["team"]["choice"])
# Expected: billing
```

Replace `VedantAndhale/laya` with `YOUR_USERNAME/YOUR_SPACE` when calling your duplicate.
For optional account authentication, store an `HF_TOKEN` secret in the calling
Space's **Settings → Variables and secrets** and construct the client with
`Client("YOUR_USERNAME/YOUR_SPACE", token=os.environ["HF_TOKEN"])` after importing
`os`. Never send the token to browser-side code or include it in a Git commit.

## API inputs and results

`state` is the text to evaluate. `questions` is a JSON string containing a non-empty
object with at most 50 named questions. Each question declares a type:

| Type | Purpose | Criteria |
| --- | --- | --- |
| `choice` | Choose an option | Object mapping option names to descriptions |
| `score` | Score against an ordered rubric | List of descriptions, lowest to highest |
| `noul` | Estimate whether a statement is true | Optional true/false descriptions |

Results contain an `answers` object keyed by your question names, plus `usage`
metadata. Choice answers include `choice`, `probabilities`, and `confidence`.
Treat probabilities as model estimates and validate them for your own use case.

`/systemone` is a **named Gradio endpoint**. For plain HTTP, use the generated
**Use via API** examples, which submit a job and read its result. Sending a POST
directly to `/systemone` or `/v1/systemone` is not this app's HTTP interface.

## Run the playground locally

Use Python 3.12 with a compatible NVIDIA GPU, CUDA-enabled PyTorch, and enough
memory for the model. This app explicitly loads on CUDA. The `spaces.GPU`
decorator does not provide a remote GPU when you run it locally.

```sh
git clone https://github.com/VedantAndhale/laya.git
cd laya
python -m venv .venv
```

Activate the environment with `.venv\Scripts\Activate.ps1` on Windows PowerShell
or `source .venv/bin/activate` on macOS/Linux, then run:

```sh
python -m pip install -r requirements.txt gradio==6.29.1
python app.py
```

Open the local URL printed in the terminal. For machines without a CUDA GPU,
call the hosted Space using `gradio_client` instead.

## Troubleshooting

| Symptom | What to check |
| --- | --- |
| Space is building or starting | Read build/runtime logs; the first startup downloads weights. |
| Space returns 404 | Check the Space name and that its visibility is Public. |
| GPU quota or queue error | Check your Hugging Face ZeroGPU quota; retry later when capacity is available. |
| CUDA error on a CPU machine | Use ZeroGPU in the Space settings, or call the hosted API from your machine. |
| Invalid questions | Use valid JSON and the criteria shape for the declared type. |
| Unexpected classification | Improve the option descriptions and evaluate representative examples. |

ZeroGPU has usage quotas and can add queue delays. It is not a dedicated,
always-on GPU service; handle unavailable predictions in your calling app.

## References

- [Hugging Face ZeroGPU](https://huggingface.co/docs/hub/spaces-zerogpu)
- [Space configuration](https://huggingface.co/docs/hub/spaces-config-reference)
- [Space visibility and secrets](https://huggingface.co/docs/hub/spaces-overview)
- [Upstream Laya](https://github.com/NandhaKishorM/laya)

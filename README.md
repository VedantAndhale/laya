---
title: Laya
emoji: "⚡"
colorFrom: pink
colorTo: blue
sdk: gradio
sdk_version: 6.29.1
python_version: '3.12'
app_file: app.py
pinned: false
license: apache-2.0
---

# Laya decision API

Public template for deploying your own Laya decision API on Hugging Face Spaces.

- [Try the public demo](https://huggingface.co/spaces/VedantAndhale/laya)
- [Use this GitHub template](https://github.com/VedantAndhale/laya/generate)
- [Setup guide](SETUP.md): duplicate the Space, customize your deployment, and call the API.

Runs the [Laya](https://github.com/NandhaKishorM/laya) decision engine and its
`convaiinnovations/laya` English checkpoint on Hugging Face ZeroGPU.
Answers typed choice, score, and noul questions with calibrated probabilities.
Laya routes and classifies requests; it does not generate code or run Ollama.

Use **Decide** in the playground or call the named Gradio API:

```python
from gradio_client import Client

client = Client("VedantAndhale/laya")
result = client.predict(
    state="I was charged twice and want a refund.",
    questions='{"team":{"type":"choice","instructions":"Which team should handle this?","criteria":{"billing":"payments and refunds","technical":"software bugs"}}}',
    api_name="/systemone",
)
print(result)
```

Install `gradio_client>=2.7.2` in the calling application. The public API can be
called without a token. For account authentication, pass your own token to
`Client(..., token=...)` from a secret or environment variable.
The Space loads model weights automatically, so no separate model server is needed.
To use a different checkpoint, set the optional `LAYA_MODEL` Space variable.

ZeroGPU allocates a GPU for each request and has usage quotas and queue delays.
This deployment is not a dedicated always-on GPU server. This Gradio deployment
exposes `/systemone` through Gradio's API, rather than the upstream FastAPI route
`/v1/systemone`. Use the Space's **Use via API** link for HTTP examples.

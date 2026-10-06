"""Laya typed decision API and playground for a Hugging Face ZeroGPU Space."""
import spaces  # Import before anything that loads torch.

import json
import os

import gradio as gr
import laya

MODEL_ID = os.environ.get("LAYA_MODEL", "convaiinnovations/laya")
agent = laya.load(MODEL_ID, device="cuda", compile=False)


@spaces.GPU(duration=30)
def decide(state, questions):
    """Evaluate choice, score and noul questions in one model pass."""
    if isinstance(questions, str):
        try:
            questions = json.loads(questions)
        except json.JSONDecodeError as exc:
            raise gr.Error("Questions must be valid JSON.") from exc
    if not isinstance(questions, dict) or not questions:
        raise gr.Error("Provide a non-empty object of typed questions.")
    if len(questions) > 50:
        raise gr.Error("Use at most 50 questions per request.")
    try:
        return agent.system_one(state, questions)
    except (ValueError, TypeError, KeyError) as exc:
        raise gr.Error(str(exc)) from exc


EXAMPLE = {
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

with gr.Blocks(title="Laya") as demo:
    gr.Markdown("# Laya\nFast typed decisions with probabilities. Enter a request and the questions to answer.")
    state = gr.Textbox(label="State", lines=5, value="I was charged twice and want a refund.")
    questions = gr.Code(label="Questions", language="json", value=json.dumps(EXAMPLE, indent=2))
    submit = gr.Button("Decide", variant="primary")
    result = gr.JSON(label="Decision")
    submit.click(decide, [state, questions], result, api_name="systemone", concurrency_limit=1)

if __name__ == "__main__":
    demo.queue(max_size=32).launch()

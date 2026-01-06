import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "mistral:7b-instruct"


def propose_causal_edges(metrics: dict) -> list[tuple[str, str]]:
    """
    Returns a list of (cause, effect) edges.
    This is a DRAFT only and must be reviewed.
    """

    metric_descriptions = "\n".join(
        [
            f"- {name}: {meta.get('description', '')}"
            + (f" Formula: {meta.get('formula')}" if "formula" in meta else "")
            for name, meta in metrics.items()
        ]
    )

    prompt = f"""
        You are helping define a DRAFT causal graph between business METRICS.

        IMPORTANT RULES:
        - ONLY use metric names listed below
        - A metric CANNOT be caused by metrics that logically depend on it
        - Do NOT assign downstream or outcome metrics as causes
        - Prefer minimal, direct causes over many weak causes
        - If unsure, OMIT the edge
        - Do NOT invent new nodes
        - Do NOT use constants, parameters, or formula variables
        - Causes and effects MUST both be valid metric names
        - Suggest ONLY direct causal relationships
        - Use metric semantics, not correlation
        - Output ONLY valid JSON in this format:

        [
        {{ "cause": "MetricA", "effect": "MetricB" }}
        ]

        VALID METRIC NAMES:
        {", ".join(metrics.keys())}

        METRIC DEFINITIONS:
        {metric_descriptions}
    """

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.2
        }
    }

    response = requests.post(OLLAMA_URL, json=payload, timeout=180)
    response.raise_for_status()

    raw = response.json()["response"].strip()

    json_block = extract_json_array(raw)

    try:
        edges = json.loads(json_block)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Invalid JSON extracted:\n{json_block}") from e

    return [(e["cause"], e["effect"]) for e in edges]

def extract_json_array(text: str) -> str:
    start = text.find("[")
    end = text.rfind("]")

    if start == -1 or end == -1 or end <= start:
        raise RuntimeError(f"No JSON array found in LLM output:\n{text}")

    return text[start:end + 1]

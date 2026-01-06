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
        You are an assistant helping to draft a CAUSAL GRAPH between business METRICS.

        This graph is used for ALERT EXPLANATION, not statistical analysis.

        Your primary goal is to produce a MINIMAL, DEFENSIBLE, NON-REDUNDANT causal structure.

        =====================
        HARD CONSTRAINTS
        =====================

        1. ONLY use metric names from the list below.
        2. Do NOT invent new metrics, parameters, constants, or formula variables.
        3. Causes and effects MUST both be valid metric names.
        4. Suggest ONLY DIRECT causal relationships (no indirect or shortcut edges).
        5. A metric MUST NOT be caused by:
        - downstream metrics
        - outcome metrics
        - metrics that logically depend on it
        6. If a causal relationship is weak, indirect, or uncertain — OMIT it.
        7. Prefer the MOST IMPORTANT cause over many weak causes.
        8. Suggest AT MOST TWO causes per metric.
        9. If a metric has no strong, defensible cause — return NO edge for it.
        10. A metric representing a population size (e.g. users, sessions) should not directly cause loss-based metrics (e.g. churn, retention).
        11. Metrics representing population size should not directly cause churn, retention, or revenue.
        
        =====================
        IMPORTANT CAUSAL RULES
        =====================

        - If A → B → C exists, do NOT add A → C.
        - If a metric explains another metric via an intermediate step, do NOT skip the step.
        - Do NOT model correlation or coincidence — only causal influence.
        - Think in terms of business explanation, not formulas.

        =====================
        OUTPUT FORMAT (STRICT)
        =====================

        Output ONLY valid JSON.
        No text, no explanations, no markdown.

        The output MUST be a JSON array of objects in this exact format:

        [
        {{ "cause": "MetricA", "effect": "MetricB" }}
        ]

        =====================
        VALID METRIC NAMES
        =====================
        {", ".join(metrics.keys())}

        =====================
        METRIC DEFINITIONS
        =====================
        {metric_descriptions}

        =====================
        TASK
        =====================

        Propose a SMALL set of high-confidence, direct causal edges.
        This is a DRAFT and will be reviewed by humans.
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

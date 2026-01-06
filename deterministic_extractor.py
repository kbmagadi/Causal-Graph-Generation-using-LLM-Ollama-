import re

def normalize_name(name: str) -> str:
    return name.lower().replace(" ", "_")


def extract_deterministic_edges(metrics: dict) -> list[tuple[str, str]]:
    """
    Extract guaranteed metric dependencies from formulas.
    Returns list of (cause, effect) edges.
    """

    edges = []
    metric_map = {
        normalize_name(name): name
        for name in metrics.keys()
    }

    for effect_metric, meta in metrics.items():
        formula = meta.get("formula")
        if not formula:
            continue

        normalized_formula = normalize_name(formula)

        for norm_name, original_name in metric_map.items():
            if norm_name in normalized_formula:
                if original_name != effect_metric:
                    edges.append((original_name, effect_metric))

    return list(set(edges)) 
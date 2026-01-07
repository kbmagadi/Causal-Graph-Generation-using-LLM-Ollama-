import re

def normalize_name(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", name.lower())


def extract_deterministic_edges(metrics: dict):
    edges = []

    normalized_metrics = {
        normalize_name(name): name
        for name in metrics.keys()
    }

    for effect, meta in metrics.items():
        formula = meta.get("formula")
        if not formula:
            continue

        norm_formula = normalize_name(formula)

        # 1️⃣ Handle division explicitly (denominator → rate)
        if "/" in formula:
            parts = formula.split("/")
            if len(parts) == 2:
                denominator = normalize_name(parts[1])

                for norm_name, original in normalized_metrics.items():
                    if norm_name == denominator:
                        edges.append((original, effect, "deterministic"))

        # 2️⃣ Handle multiplication (all inputs cause output)
        if "*" in formula:
            for norm_name, original in normalized_metrics.items():
                if norm_name in norm_formula and original != effect:
                    edges.append((original, effect, "deterministic"))

    return list(set(edges))

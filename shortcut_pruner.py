from collections import defaultdict

RATE_KEYWORDS = ["rate", "ratio", "percentage"]

def prune_shortcut_edges(edges, metrics):
    """
    Remove edges that skip an intermediate deterministic dependency.
    """

    deterministic_deps = extract_formula_dependencies(metrics)

    # Build effect lookup
    causes_of = {}
    for src, dst, edge_type in edges:
        causes_of.setdefault(dst, []).append((src, edge_type))

    pruned = []

    for src, dst, edge_type in edges:
        # Only prune LLM edges
        if edge_type != "llm":
            pruned.append((src, dst, edge_type))
            continue

        # If src depends on some X, and X -> dst exists, prune src -> dst
        intermediates = deterministic_deps.get(src, [])

        shortcut_found = False
        for mid in intermediates:
            for cause, _ in causes_of.get(dst, []):
                if cause == mid:
                    print(
                        f"✂️ Pruned shortcut edge: {src} → {dst} (via {mid})"
                    )
                    shortcut_found = True
                    break

            if shortcut_found:
                break

        if not shortcut_found:
            pruned.append((src, dst, edge_type))

    return pruned

def extract_formula_dependencies(metrics):
    deps = {}
    for metric, meta in metrics.items():
        formula = meta.get("formula", "")
        formula_l = formula.lower()
        parents = []
        for other in metrics:
            if other.lower() in formula_l and other != metric:
                parents.append(other)
        deps[metric] = parents
    return deps

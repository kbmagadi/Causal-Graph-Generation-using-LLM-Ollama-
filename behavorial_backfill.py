SAFE_BACKFILL_RULES = {
    "churn": ["engagement", "support", "satisfaction"],
    "retained": ["churn"],
    "revenue": ["orders", "retained", "average revenue"],
    "mrr": ["retained", "average revenue"]
}

def backfill_behavioral_causes(edges, metrics):
    """
    Restore missing causal parents for derived metrics
    WITHOUT introducing cycles.
    """

    causes_by_effect = {}
    for src, dst in edges:
        causes_by_effect.setdefault(dst, set()).add(src)

    new_edges = set(edges)

    metric_names = list(metrics.keys())

    for metric in metric_names:
        # Skip base metrics
        if metrics[metric].get("type") == "base":
            continue

        # Skip if it already has causes
        if metric in causes_by_effect and causes_by_effect[metric]:
            continue

        metric_l = metric.lower()

        for key, allowed_sources in SAFE_BACKFILL_RULES.items():
            if key in metric_l:
                for src in metric_names:
                    src_l = src.lower()
                    if any(a in src_l for a in allowed_sources):
                        if src != metric:
                            new_edges.add((src, metric))

    return list(new_edges)

SAFE_BACKFILL_RULES = {
    "churn": ["engagement", "support", "satisfaction"],
    "retained": ["churn"],
    "revenue": ["orders", "retained", "average revenue"],
    "mrr": ["retained", "average revenue"]
}

def backfill_behavioral_causes(edges, metrics):
    causes_by_effect = {}
    for edge in edges:
        if len(edge) == 3:
            src, dst, _ = edge
        else:
            src, dst = edge
        causes_by_effect.setdefault(dst, set()).add(src)

    new_edges = set(edges)
    metric_names = list(metrics.keys())

    for metric in metric_names:
        if metrics[metric].get("type") == "base":
            continue
        if metric in causes_by_effect and causes_by_effect[metric]:
            continue

        metric_l = metric.lower()

        for key, allowed_sources in SAFE_BACKFILL_RULES.items():
            if key in metric_l:
                for src in metric_names:
                    src_l = src.lower()
                    if any(a in src_l for a in allowed_sources):
                        if src != metric:
                            new_edges.add((src, metric, "safe_backfill"))

    return list(new_edges)
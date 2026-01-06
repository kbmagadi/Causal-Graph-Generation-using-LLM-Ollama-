def normalize_edges(edges, valid_metrics):
    cleaned = set()

    for src, dst in edges:
        src = src.strip()
        dst = dst.strip()

        # Filter out non-metric nodes
        if src not in valid_metrics or dst not in valid_metrics:
            continue

        if src != dst:
            cleaned.add((src, dst))

    return list(cleaned)

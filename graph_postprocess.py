def normalize_edges(edges, valid_metrics):
    cleaned = {}

    for edge in edges:
        if len(edge) == 3:
            src, dst, source = edge
        elif len(edge) == 2:
            src, dst = edge
            source = "unknown"
        else:
            raise ValueError(f"Invalid edge shape: {edge}")

        src = src.strip()
        dst = dst.strip()

        if src not in valid_metrics or dst not in valid_metrics:
            continue
        if src == dst:
            continue

        cleaned[(src, dst)] = source  # keep last-seen source

    return [(src, dst, source) for (src, dst), source in cleaned.items()]
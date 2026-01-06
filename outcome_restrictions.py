def enforce_outcome_restrictions(edges, metrics):
    outcomes = {
        name for name, meta in metrics.items()
        if meta.get("role") == "outcome"
    }

    restricted = []

    for src, dst in edges:
        if src in outcomes:
            print(f"❌ Outcome metric cannot be a cause: {src} → {dst}")
            continue
        restricted.append((src, dst))

    return restricted

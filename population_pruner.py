POPULATION_KEYWORDS = ["users", "sessions", "traffic", "visits"]
LOSS_KEYWORDS = ["churn", "retained"]

def prune_population_causes(edges):
    pruned = []

    for src, dst, edge_type in edges:
        # 🚨 NEVER prune deterministic edges
        if edge_type == "deterministic":
            pruned.append((src, dst, edge_type))
            continue

        src_l = src.lower()
        dst_l = dst.lower()

        if any(k in src_l for k in POPULATION_KEYWORDS) and \
           any(k in dst_l for k in LOSS_KEYWORDS):
            print(f"❌ Pruned population-size edge: {src} → {dst}")
            continue

        pruned.append((src, dst, edge_type))

    return pruned

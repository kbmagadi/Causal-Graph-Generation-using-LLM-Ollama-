# pruning/population_pruner.py

POPULATION_KEYWORDS = ["users", "sessions", "traffic", "visits"]
LOSS_KEYWORDS = ["churn", "retained"]

def prune_population_causes(edges):
    """
    Remove edges where population-size metrics are incorrectly
    treated as causes of loss-based or outcome metrics.
    """
    pruned = []

    for src, dst in edges:
        src_l = src.lower()
        dst_l = dst.lower()

        if any(k in src_l for k in POPULATION_KEYWORDS) and \
           any(k in dst_l for k in LOSS_KEYWORDS):
            print(f"❌ Pruned population-size edge: {src} → {dst}")
            continue

        pruned.append((src, dst))

    return pruned

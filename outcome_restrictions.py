RATE_KEYWORDS = ["rate", "percentage", "ratio"]

OUTCOME_KEYWORDS = [
    "orders",
    "revenue",
    "retained",
    "users",
    "sessions"
]

def enforce_outcome_restrictions(edges, metrics):
    pruned = []

    for src, dst, edge_type in edges:
        # NEVER prune deterministic edges
        if edge_type == "deterministic":
            pruned.append((src, dst, edge_type))
            continue

        src_l = src.lower()
        dst_l = dst.lower()

        # Outcome → Rate is invalid
        if "rate" in dst_l:
            if any(k in src_l for k in ["revenue", "orders", "retained", "churn"]):
                print(f"✂️ Pruned invalid outcome → rate edge: {src} → {dst}")
                continue

        pruned.append((src, dst, edge_type))

    return pruned
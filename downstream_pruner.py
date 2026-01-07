def prune_downstream_causes(edges, metrics):
    pruned = []
    roles = {name: meta.get("role") for name, meta in metrics.items()}

    ROLE_ORDER = {"base": 0, "intermediate": 1, "outcome": 2}

    for src, dst, edge_type in edges:
        # 🚨 NEVER prune deterministic edges
        if edge_type == "deterministic":
            pruned.append((src, dst, edge_type))
            continue

        src_role = ROLE_ORDER.get(roles.get(src), 1)
        dst_role = ROLE_ORDER.get(roles.get(dst), 1)

        if src_role > dst_role:
            print(f"❌ Pruned downstream edge: {src} → {dst}")
            continue

        pruned.append((src, dst, edge_type))

    return pruned

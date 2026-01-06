def prune_downstream_causes(edges, metrics):
    """
    Removes edges where effect logically precedes cause
    based on metric roles.
    """
    pruned = []
    roles = {
        name: meta.get("role")
        for name, meta in metrics.items()
    }

    ROLE_ORDER = {
        "base": 0,
        "intermediate": 1,
        "outcome": 2
    }

    for src, dst in edges:
        src_role = ROLE_ORDER.get(roles.get(src), 1)
        dst_role = ROLE_ORDER.get(roles.get(dst), 1)

        # downstream → upstream (invalid)
        if src_role > dst_role:
            print(f"❌ Pruned downstream edge: {src} → {dst}")
            continue

        pruned.append((src, dst))

    return pruned
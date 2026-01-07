EDGE_PRIORITY = {
    "deterministic": 999,
    "safe_backfill": 2,
    "llm": 1,
    "heuristic_backfill": 0,
}

def resolve_cycles(edges, detect_cycle_fn):
    """
    Iteratively resolves cycles by removing the weakest edge
    involved in each detected cycle.

    Deterministic edges are NEVER removed.
    """

    edges = list(edges)

    while True:
        cycle = detect_cycle_fn(edges)

        if not cycle:
            break  # ✅ no cycles left

        print(f"⚠️ Causal cycle detected: {' -> '.join(cycle)}")

        # Collect edges involved in the cycle
        cycle_edges = []
        cycle_nodes = set(cycle)

        for src, dst, edge_type in edges:
            if src in cycle_nodes and dst in cycle_nodes:
                cycle_edges.append((src, dst, edge_type))

        # Separate deterministic vs removable edges
        removable = [
            e for e in cycle_edges if e[2] != "deterministic"
        ]

        if not removable:
            raise RuntimeError(
                "❌ Deterministic-only causal cycle detected. "
                "This indicates a bug in deterministic extraction."
            )

        # Drop the weakest removable edge
        weakest = min(
            removable,
            key=lambda e: EDGE_PRIORITY.get(e[2], 0)
        )

        print(
            f"✂️ Breaking cycle by dropping edge: "
            f"{weakest[0]} → {weakest[1]} ({weakest[2]})"
        )

        edges.remove(weakest)

    return edges

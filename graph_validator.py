def validate_graph(edges, metrics):
    metric_names = set(metrics.keys())

    # 1. Validate nodes
    for src, dst in edges:
        if src not in metric_names:
            raise ValueError(f"Unknown cause metric: {src}")
        if dst not in metric_names:
            raise ValueError(f"Unknown effect metric: {dst}")
        if src == dst:
            raise ValueError(f"Self-causation detected for metric: {src}")

    # 2. Build adjacency list (cause -> effect)
    graph = {}
    for src, dst in edges:
        graph.setdefault(src, []).append(dst)

    # 3. Cycle detection (DFS)
    visited = set()
    rec_stack = set()

    def dfs(node):
        if node in rec_stack:
            raise ValueError(f"Causal cycle detected involving metric: {node}")

        if node in visited:
            return

        visited.add(node)
        rec_stack.add(node)

        for neighbor in graph.get(node, []):
            dfs(neighbor)

        rec_stack.remove(node)

    # Run DFS on all nodes
    for metric in metric_names:
        if metric not in visited:
            dfs(metric)

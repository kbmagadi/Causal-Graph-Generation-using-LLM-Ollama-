def validate_graph(edges, metrics):
    """
    Validates:
    1. All nodes exist
    2. No self loops
    3. Graph is acyclic (cycle detection handled separately)
    """

    metric_names = set(metrics.keys())

    # 1. Validate nodes
    for src, dst, _ in edges:
        if src not in metric_names:
            raise ValueError(f"Unknown cause metric: {src}")
        if dst not in metric_names:
            raise ValueError(f"Unknown effect metric: {dst}")
        if src == dst:
            raise ValueError(f"Self-causation detected for metric: {src}")

def detect_cycle(edges):
    """
    Detects a cycle in the graph.
    Returns the cycle path as a list of nodes if found, else None.
    """

    # Build adjacency list
    graph = {}
    for src, dst, _ in edges:
        graph.setdefault(src, []).append(dst)

    visited = set()
    stack = []

    def dfs(node):
        if node in stack:
            # return the cycle path
            cycle_start_index = stack.index(node)
            return stack[cycle_start_index:] + [node]

        if node in visited:
            return None

        visited.add(node)
        stack.append(node)

        for neighbor in graph.get(node, []):
            cycle = dfs(neighbor)
            if cycle:
                return cycle

        stack.pop()
        return None

    for node in graph:
        cycle = dfs(node)
        if cycle:
            return cycle

    return None

from collections import defaultdict

def detect_redundant_edges(edges):
    graph = defaultdict(set)
    for src, dst in edges:
        graph[src].add(dst)

    redundant = []

    for a in graph:
        for b in graph[a]:
            for c in graph.get(b, []):
                if c in graph[a]:
                    redundant.append((a, c))

    return list(set(redundant))

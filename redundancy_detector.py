from collections import defaultdict

def detect_redundant_edges(edges):
    graph = defaultdict(set)
    for edge in edges:
        src, dst = edge[0], edge[1]
        graph[src].add(dst)

    redundant = []
    for a in graph:
        for b in graph[a]:
            for c in graph.get(b, []):
                if c in graph[a]:
                    redundant.append((a, c))

    return list(set(redundant))
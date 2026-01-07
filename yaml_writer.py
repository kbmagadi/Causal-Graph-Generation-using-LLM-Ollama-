import yaml
from collections import defaultdict

def write_graph(edges, all_metrics, path):
    graph = defaultdict(list)

    for cause, effect, *_ in edges:
        graph[effect].append(cause)

    for metric in all_metrics:
        graph.setdefault(metric, [])

    output = {
        "metrics": {
            metric: {"causes": graph[metric]}
            for metric in sorted(graph.keys())
        }
    }

    with open(path, "w") as f:
        yaml.dump(output, f, sort_keys=False)
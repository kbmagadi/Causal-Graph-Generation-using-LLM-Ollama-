import yaml
from collections import defaultdict

def write_graph(edges, all_metrics, path):
    graph = defaultdict(list)

    # Populate causes from edges
    for cause, effect in edges:
        graph[effect].append(cause)

    # Ensure all metrics are present (base metrics get empty causes)
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

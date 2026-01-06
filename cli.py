import argparse
from metric_loader import load_metrics
from ollama_causal_proposer import propose_causal_edges
from graph_postprocess import normalize_edges
from graph_validator import validate_graph
from yaml_writer import write_graph


def main():
    parser = argparse.ArgumentParser(description="Generate DRAFT causal graph")
    parser.add_argument("--metrics", required=True)
    parser.add_argument("--output", required=True)

    args = parser.parse_args()

    metrics = load_metrics(args.metrics)

    edges = propose_causal_edges(metrics)
    edges = normalize_edges(edges, metrics.keys())  
    validate_graph(edges, metrics)

    write_graph(edges, metrics.keys(), args.output)

    print(f"Draft causal graph written to {args.output}")

if __name__ == "__main__":
    main()

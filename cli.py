import argparse
from metric_loader import load_metrics
from ollama_causal_proposer import propose_causal_edges
from graph_postprocess import normalize_edges
from graph_validator import validate_graph
from yaml_writer import write_graph
from deterministic_extractor import extract_deterministic_edges

def main():
    parser = argparse.ArgumentParser(description="Generate DRAFT causal graph")
    parser.add_argument("--metrics", required=True)
    parser.add_argument("--output", required=True)

    args = parser.parse_args()

    metrics = load_metrics(args.metrics)

    # 1. Deterministic edges (mandatory)
    deterministic_edges = extract_deterministic_edges(metrics)

    print("Deterministic edges:")
    for e in deterministic_edges:
        print("  ", e)

    # 2. LLM-suggested edges (optional)
    llm_edges = propose_causal_edges(metrics)

    # 3. Merge (deterministic edges always included)
    all_edges = list(set(deterministic_edges + llm_edges))

    # 4. Normalize & filter
    all_edges = normalize_edges(all_edges, metrics.keys())

    # 5. Validate structure
    validate_graph(all_edges, metrics)

    # 6. Write output
    write_graph(all_edges, metrics.keys(), args.output)

    print(f"Draft causal graph written to {args.output}")

if __name__ == "__main__":
    main()

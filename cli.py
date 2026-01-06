import argparse
from metric_loader import load_metrics
from deterministic_extractor import extract_deterministic_edges
from ollama_causal_proposer import propose_causal_edges
from graph_postprocess import normalize_edges
from downstream_pruner import prune_downstream_causes
from population_pruner import prune_population_causes
from outcome_restrictions import enforce_outcome_restrictions
from redundancy_detector import detect_redundant_edges
from graph_validator import validate_graph
from yaml_writer import write_graph
from behavorial_backfill import backfill_behavioral_causes


def main():
    parser = argparse.ArgumentParser(description="Generate DRAFT causal graph")
    parser.add_argument("--metrics", required=True)
    parser.add_argument("--output", required=True)

    args = parser.parse_args()

    metrics = load_metrics(args.metrics)

    # Merge deterministic + LLM edges
    deterministic_edges = extract_deterministic_edges(metrics)
    llm_edges = propose_causal_edges(metrics)
    all_edges = list(set(deterministic_edges + llm_edges))

    # Normalize
    all_edges = normalize_edges(all_edges, metrics.keys())

    # Hard pruning
    all_edges = prune_population_causes(all_edges)
    all_edges = prune_downstream_causes(all_edges, metrics)
    all_edges = enforce_outcome_restrictions(all_edges, metrics)

    # Behavorial backfill
    all_edges = backfill_behavioral_causes(all_edges, metrics)
    # Structural validation
    validate_graph(all_edges, metrics)

    # Redundancy warning (soft)
    redundant = detect_redundant_edges(all_edges)
    if redundant:
        print(f"⚠️ Redundant edges detected (ignore if intentional): {redundant}")

    # Write output
    write_graph(all_edges, metrics.keys(), args.output)

    print(f"Draft causal graph written to {args.output}")


if __name__ == "__main__":
    main()
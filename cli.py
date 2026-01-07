import argparse
from metric_loader import load_metrics
from deterministic_extractor import extract_deterministic_edges
from ollama_causal_proposer import propose_causal_edges
from graph_postprocess import normalize_edges
from downstream_pruner import prune_downstream_causes
from population_pruner import prune_population_causes
from shortcut_pruner import prune_shortcut_edges
from outcome_restrictions import enforce_outcome_restrictions
from behavorial_backfill import backfill_behavioral_causes
from redundancy_detector import detect_redundant_edges
from graph_validator import validate_graph, detect_cycle
from cycle_resolver import resolve_cycles
from yaml_writer import write_graph


def main():
    parser = argparse.ArgumentParser(description="Generate DRAFT causal graph")
    parser.add_argument("--metrics", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    # Load metrics
    metrics = load_metrics(args.metrics)

    # 1. Deterministic + LLM edges
    deterministic_edges = extract_deterministic_edges(metrics)
    llm_edges = propose_causal_edges(metrics)
    all_edges = list(set(deterministic_edges + llm_edges))

    # 2. Normalize
    all_edges = normalize_edges(all_edges, metrics.keys())

    # 3. Hard pruning
    all_edges = prune_population_causes(all_edges)
    all_edges = prune_downstream_causes(all_edges, metrics)
    all_edges = enforce_outcome_restrictions(all_edges, metrics)

    # 4. Behavioral backfill
    all_edges = backfill_behavioral_causes(all_edges, metrics)

    # 5. Remove transitive shortcut edges
    all_edges = prune_shortcut_edges(all_edges, metrics)

    # 6. 🔁 Resolve cycles ONCE, correctly
    all_edges = resolve_cycles(all_edges, detect_cycle)

    # 7. Final validation (now guaranteed acyclic)
    validate_graph(all_edges, metrics)

    # 8. Redundancy warning (soft)
    redundant = detect_redundant_edges(all_edges)
    if redundant:
        print(f"⚠️ Redundant edges detected (ignore if intentional): {redundant}")

    # 9. Write output
    write_graph(all_edges, metrics.keys(), args.output)

    print(f"Draft causal graph written to {args.output}")


if __name__ == "__main__":
    main()

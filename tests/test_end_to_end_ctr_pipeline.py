def test_ctr_pipeline_end_to_end():
    metrics = {
        "Impressions": {"type": "base"},
        "Clicks": {"type": "derived", "formula": "impressions * ctr"},
        "Click Through Rate": {"type": "derived", "formula": "clicks / impressions"},
        "Signups": {"type": "derived", "formula": "clicks * conversion"},
    }

    from deterministic_extractor import extract_deterministic_edges
    from downstream_pruner import prune_downstream_causes
    from outcome_restrictions import enforce_outcome_restrictions
    from graph_validator import detect_cycle
    from cycle_resolver import resolve_cycles

    edges = extract_deterministic_edges(metrics)
    edges = prune_downstream_causes(edges, metrics)
    edges = enforce_outcome_restrictions(edges, metrics)
    edges = resolve_cycles(edges, detect_cycle)

    # Must exist
    assert ("Impressions", "Click Through Rate", "deterministic") in edges
    assert ("Clicks", "Signups", "deterministic") in edges

    # Must NOT exist
    assert ("Click Through Rate", "Signups", "llm") not in edges

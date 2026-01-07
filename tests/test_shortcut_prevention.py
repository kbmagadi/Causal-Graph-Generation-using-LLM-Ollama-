def test_rate_does_not_skip_intermediate_metric():
    metrics = {
        "Impressions": {"type": "base"},
        "Clicks": {"type": "derived", "formula": "impressions * ctr"},
        "Click Through Rate": {"type": "derived", "formula": "clicks / impressions"},
        "Signups": {"type": "derived", "formula": "clicks * conversion"},
    }

    from ollama_causal_proposer import propose_causal_edges
    from shortcut_pruner import prune_shortcut_edges


    edges = [
        ("Click Through Rate", "Signups", "llm"),
        ("Clicks", "Signups", "deterministic"),
    ]

    pruned = prune_shortcut_edges(edges, metrics)

    assert (
        "Click Through Rate",
        "Signups",
        "llm",
    ) not in pruned, "Rate → downstream shortcut edge was not pruned"

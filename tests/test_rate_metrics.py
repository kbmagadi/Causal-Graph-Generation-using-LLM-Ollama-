def test_denominator_preserved_for_rate():
    metrics = {
        "Impressions": {"type": "base"},
        "Clicks": {"type": "derived", "formula": "impressions * ctr"},
        "Click Through Rate": {"type": "derived", "formula": "clicks / impressions"},
    }

    from deterministic_extractor import extract_deterministic_edges
    from outcome_restrictions import enforce_outcome_restrictions

    edges = extract_deterministic_edges(metrics)
    edges = enforce_outcome_restrictions(edges, metrics)

    assert (
        "Impressions",
        "Click Through Rate",
        "deterministic",
    ) in edges, "Denominator → Rate edge was incorrectly pruned"

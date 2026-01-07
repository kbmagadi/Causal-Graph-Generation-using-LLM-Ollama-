def test_activation_rate_has_signup_parent():
    metrics = {
        "Signups": {"type": "derived"},
        "Activation Rate": {
            "type": "derived",
            "formula": "activated_users / signups",
        },
    }

    from deterministic_extractor import extract_deterministic_edges

    edges = extract_deterministic_edges(metrics)

    assert (
        "Signups",
        "Activation Rate",
        "deterministic",
    ) in edges, "Activation Rate lost its denominator dependency"

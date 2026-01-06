import yaml

def load_metrics(path: str) -> dict:
    with open(path) as f:
        data = yaml.safe_load(f)
    return data["metrics"]

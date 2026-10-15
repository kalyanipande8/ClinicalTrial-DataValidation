import json
import os

from src.simulate_trial_data import simulate
from src.endpoint_derivation import derive_all_endpoints
from src.validation import validate_endpoint_accuracy


def main():
    df = simulate()
    derived = derive_all_endpoints(df)
    result = validate_endpoint_accuracy(derived)

    os.makedirs("results", exist_ok=True)
    derived.to_csv("results/derived_endpoints.csv", index=False)
    with open("results/summary.json", "w") as f:
        json.dump(result, f, indent=2)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

"""
Helper script to pre-generate all word biases as a big JSON, so the server doesn't need as much memory to run
"""

import json
from os import path
from PcaBiasCalculator import PcaBiasCalculator
import statistics
import numpy as np


def preprocess_biases():
    print("creating calculator")
    calculator = PcaBiasCalculator()
    print("mapping biases")
    bias_mapping = {}
    count = 0
    total_keys = len(calculator.keys())
    for word in calculator.keys():
        bias_mapping[word] = calculator.detect_bias(word)
        count += 1
        if count % 100000 == 0:
            print(f"done: {count} / {total_keys}")

    # debug stats
    #vals = [v for v in bias_mapping.values() if isinstance(v, (int,float))]
    #print("bias stats: count", len(vals), "min", min(vals), "q1", np.percentile(vals,25), "median", np.median(vals), "mean", statistics.mean(vals), "q3", np.percentile(vals,75), "max", max(vals))

    print("writing biases")
    output_file = path.join(path.dirname(__file__), "data/biases.json")
    with open(output_file, "w") as outfile:
        json.dump(bias_mapping, outfile, ensure_ascii=False, indent=2)
    print("done!")


if __name__ == "__main__":
    preprocess_biases()

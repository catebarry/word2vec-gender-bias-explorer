import re
import json
from os import path


class PrecalculatedBiasCalculator:
    """
    Helper around loading and using pre-calculated biases
    Useful in production to save server memory
    """
    '''
    def __init__(
        self, bias_json=path.join(path.dirname(__file__), "data/biases.json")
    ):
        with open(bias_json) as json_file:
            self.biases = json.load(json_file)
    '''
    
    # added for compressed file support
    def __init__(self, bias_json=None):
        base_dir = path.dirname(__file__)
        data_dir = path.join(base_dir, "data")

        # Default path to uncompressed file
        default_json = path.join(data_dir, "biases.json")
        # Corresponding compressed file
        gz_path = default_json + ".gz"

        # Use whichever exists (prefer uncompressed for speed)
        if bias_json is None:
            if path.exists(default_json):
                bias_json = default_json
            elif path.exists(gz_path):
                # Decompress once if needed
                print("Decompressing biases.json.gz...", flush=True)
                with gzip.open(gz_path, "rb") as f_in:
                    data = f_in.read()
                with open(default_json, "wb") as f_out:
                    f_out.write(data)
                print("Decompression complete.", flush=True)
                bias_json = default_json
            else:
                raise FileNotFoundError(
                    f"Neither {default_json} nor {gz_path} found."
                )

        # Load the JSON file
        with open(bias_json, "r", encoding="utf-8") as json_file:
            self.biases = json.load(json_file)

    def detect_bias(self, raw_word):
        word = re.sub(r"\s+", "_", raw_word)
        if word not in self.biases:
            return None
        return self.biases[word]

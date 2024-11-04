import ir_datasets as irds  
import pandas as pd
from fire import Fire

def sample(dataset_id : str, out_file : str, subset : int = -1):
    dataset = irds.load(dataset_id)
    assert dataset.has_docpairs(), "Dataset must have docpairs! Make sure you're not using a test collection"
    df = pd.DataFrame(dataset.docpairs_iter())
    df = df.sample(n=subset) if subset > 0 else df
    df.to_json(out_file, orient='records', lines=True)
    return f"Successfully took subset of {dataset_id} of size {len(df)} and saved to {out_file}"

if __name__ == '__main__':
    Fire(sample)
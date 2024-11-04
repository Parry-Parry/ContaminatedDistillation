import ir_datasets as irds 
import pandas as pd
from fire import Fire
import random
from tqdm import tqdm
import logging

def convert_qrels(dataset : str, out_dir : str, rel : int = 2, hard : bool = False, n_neg : int = 1):
    dataset = irds.load(dataset)
    qrels = pd.DataFrame(dataset.qrels_iter())

    positives = qrels[qrels['relevance'] >= rel]
    negatives = qrels[qrels['relevance'] < rel].groupby('query_id')['doc_id'].apply(list).to_dict()
    # flatten negatives
    all_docs = [
        doc_id for docs in negatives.values() for doc_id in docs
    ]
    frame = {
        'query_id': [],
        'doc_id_a': [],
        'doc_id_b': [],
    }

    for row in tqdm(positives.itertuples()):
        frame['query_id'].append(row.query_id)
        frame['doc_id_a'].append(row.doc_id)
        # pop a negative from negatives
        if hard:
            if len(negatives[row.query_id]) > 0:
                frame['doc_id_b'].append(negatives[row.query_id].pop(0))
            else:
                # random sample a negative from any 
                frame['doc_id_b'].append(random.choice(all_docs))
        else:
            # random sample a negative from any 
            frame['doc_id_b'].append(random.choice(all_docs) if n_neg == 1 else random.sample(all_docs, k=n_neg))                                                                                             

    frame = pd.DataFrame(frame)[['query_id', 'doc_id_a', 'doc_id_b']]                                                                           
    frame.to_json(out_dir, orient='records', lines=True)

    return f"Successfully converted qrels from {dataset} to {out_dir}"

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    Fire(convert_qrels)

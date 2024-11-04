import pandas as pd 
import ir_datasets as irds

def combine_qrels(qrel_triples : str, out_dir : str, main_triples : str = None, ir_dataset : str = None):
    assert main_triples is not None or ir_dataset is not None, "Either main_triples or ir_dataset must be provided."

    qrel_triples = pd.read_json(qrel_triples, lines=True, orient='records')

    if main_triples:
        main_triples = pd.read_json(main_triples, lines=True, orient='records')
    else:
        main_triples = pd.DataFrame(irds.load(ir_dataset).docpairs_iter())
    
    triples = pd.concat([qrel_triples, main_triples], ignore_index=True)[['query_id', 'doc_id_a', 'doc_id_b']]

    triples.to_json(out_dir, orient='records', lines=True)

    return f"Successfully combined qrels from qrel_triples and main_triples to {out_dir}"

if __name__ == '__main__':
    import fire
    fire.Fire(combine_qrels)
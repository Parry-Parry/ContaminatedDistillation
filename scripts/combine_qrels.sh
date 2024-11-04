type=$1

python -m contaminate.data.combine_qrels --dataset msmarco-passage/trec-dl-20${type}/judged --qrel_triples data/qrels.${type}.jsonl.gz --main_triples data/triples.jsonl.gz --out_dir data/combined.${type}.jsonl.gz
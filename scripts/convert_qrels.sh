type=$1

python -m contaminate.data.convert_qrels --dataset msmarco-passage/trec-dl-20${type}/judged --out_dir data/qrels.${type}.jsonl.gz --hard  
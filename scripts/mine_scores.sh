
type=$1

python -m contaminate.data.mine_negatives --file data/triples.jsonl.gz --index_path msmarco-passage --dataset msmarco-passage/train/triples-small --model_name_or_path checkpoints/${type}_teacher --out_dir data/${type}.negatives.jsonl.gz --architecture cat
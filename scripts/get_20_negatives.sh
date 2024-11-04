group_size=$1

python -m contaminate.data.negatives_from_lookup --triples_file data/triples.jsonl.gz --score_file data_20/teacher_scores.json --out_file data_20/conta.${group_size}.triples.jsonl.gz --group_size $group_size

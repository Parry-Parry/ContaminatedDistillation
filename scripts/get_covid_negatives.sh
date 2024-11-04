group_size=$1

python -m contaminate.data.negatives_from_lookup --triples_file data/triples.jsonl.gz --score_file data_covid/teacher_scores.json --out_file data_covid/conta.${group_size}.triples.jsonl.gz --group_size $group_size

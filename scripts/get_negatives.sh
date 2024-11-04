teacher=$1
group_size=$2

python -m contaminate.data.negatives_from_lookup --triples_file data/triples.jsonl.gz --score_file data/${teacher}.scores.json.gz --out_file data/${teacher}.${group_size}.triples.jsonl.gz --group_size $group_size

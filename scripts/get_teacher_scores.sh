
type=$1

python -m contaminate.data.get_teacher_scores --triples_dir data/triples.jsonl.gz --model_name_or_path checkpoints/${type}_teacher --ir_dataset msmarco-passage/train/triples-small --output_file data/${type}.scores.jsonl.gz --architecture cat
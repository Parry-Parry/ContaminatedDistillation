type=$1
eval=$2

python -m contaminate.run_topics --model_name_or_path checkpoints_${type}/conta --ir_dataset msmarco-passage/trec-dl-20${eval}/judged --topics_or_res data/bm25_${eval}.txt --out_path runs/conta_student_${type}_${eval}.tsv.gz --cat
python -m contaminate.run_topics --model_name_or_path checkpoints_${type}/standard --ir_dataset msmarco-passage/trec-dl-20${eval}/judged --topics_or_res data/bm25_${eval}.txt --out_path runs/standard_student_${type}_${eval}.tsv.gz --cat
python -m contaminate.evaluate --eval msmarco-passage/trec-dl-20${eval}/judged --run_dir runs --out_dir metrics/student_${eval}.tsv --rel 2
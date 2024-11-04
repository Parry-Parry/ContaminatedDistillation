
python -m contaminate.run_topics --model_name_or_path checkpoints/conta_teacher --ir_dataset msmarco-passage/trec-dl-2019/judged --topics_or_res data/bm25.txt --out_path runs/conta.tsv.gz --cat
python -m contaminate.run_topics --model_name_or_path checkpoints/standard_teacher --ir_dataset msmarco-passage/trec-dl-2019/judged --topics_or_res data/bm25.txt --out_path runs/standard.tsv.gz --cat
python -m contaminate.evaluate --eval msmarco-passage/trec-dl-2019/judged --run_dir runs --out_dir metrics/teacher.tsv --rel 2
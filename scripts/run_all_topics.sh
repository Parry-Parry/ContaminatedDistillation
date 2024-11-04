#!/usr/bin/env bash
DATASETS=("msmarco-passage/trec-dl-2019/judged" "msmarco-passage/trec-dl-2020/judged" "beir/trec-covid")

for dataset in "${DATASETS[@]}"; do 
    python -m contaminate.batch_run_topics \
        --model_directory checkpoints \
        --ir_dataset $dataset \
        --output_directory runs 
    done

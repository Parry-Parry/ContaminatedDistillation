#!/usr/bin/env bash

for dataset in "${DATASETS[@]}"; do 
    python -m contaminate.batch_run_topics \
        --model_directory checkpoints \
        --ir_dataset beir/trec-covid \
        --output_directory runs \
        --topics_or_res data/bm25.covid.100.tsv.gz
    done

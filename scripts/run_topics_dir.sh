model_dir=$1
dataset=$2
topics_or_res=$3
out_dir=$4


python -m contaminate.batch_run_topics --model_directory $model_dir --ir_dataset $dataset --topics_or_res data/$topics_or_res --output_directory $out_dir
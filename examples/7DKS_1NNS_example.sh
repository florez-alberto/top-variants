#!/bin/bash
#SBATCH --mem=20g
#SBATCH -c 3
#SBATCH --output=example_1.out

output_dir="../output/example_7DKS_1NNS_outputs"

if [ ! -d $output_dir ]
then
    mkdir -p $output_dir
fi

# for k=1, DKS,NNS and 7,1 positions and full coverage size=200,000
python3 ../top_variants.py \
        --output_dir $output_dir \
        --degeneracy_strategy_list "DKS,NNS" \
        --counts_list "7,1" \
        --library_size 200000 \
        --print_interval 1000000 \
        --log_output 

sleep 5
python3 ../top_variants.py \
        --output_dir $output_dir \
        --get_top_k_variants \
        --probability_T1 0.0009675479282818195 \
        --ks_list "1,10,100,1000"

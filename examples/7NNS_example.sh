#!/bin/bash
#SBATCH --mem=20g
#SBATCH -c 3
#SBATCH --output=example_1.out

output_dir="../output/example_7NNS_outputs"

#for k=1, NNN, and 3 positions and full coverage size=1,344,623

if [ ! -d $output_dir ]
then
    mkdir -p $output_dir
fi

# for k=1, NNS, and 7 positions and full coverage size=200,000
python3 ../top_variants.py \
        --output_dir $output_dir \
        --degeneracy_strategy_list "NNS" \
        --counts_list "7" \
        --library_size 200000 \
        --print_interval 1000000 \
        --log_output 

sleep 5
#given the output of the above command, we can now get the top k variants
python3 ../top_variants.py \
        --output_dir $output_dir \
        --get_top_k_variants \
        --probability_T1 0.00012507996569778484 \
        --ks_list "1,10,100,1000"

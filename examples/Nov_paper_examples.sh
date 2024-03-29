#!/bin/bash
#SBATCH --mem=20g
#SBATCH -c 3
#SBATCH --output=example_1.out

output_dir="../output/example_1_outputs"


if [ ! -d $output_dir ]
then
    mkdir -p $output_dir
fi

#"for k=1, NNN, and 2 positions and 95% prob: size=5,525"
python3 ../top_variants.py \
        --output_dir $output_dir \
        --degeneracy_strategy_list "NNN" \
        --counts_list "2" \
        --library_size 5525 \
        --print_interval 100 \
        --log_output 
sleep 5
#"for k=1, NNN, and 2 positions and 99% prob=2,738"
python3 ../top_variants.py \
        --output_dir $output_dir \
        --degeneracy_strategy_list "NNN" \
        --counts_list "2" \
        --library_size 2738 \
        --print_interval 100 \
        --log_output

sleep 5
#"for k=1, NNN, and 3 positions and 95% prob=79,041"     
python3 ../top_variants.py \
        --output_dir $output_dir \
        --degeneracy_strategy_list "NNN" \
        --counts_list "3" \
        --library_size 79041 \
        --print_interval 1000 \
        --log_output 

sleep 5

#"for k=1, NNN, and 3 positions and 99% prob: size=175,835"
python3 ../top_variants.py \
        --output_dir $output_dir \
        --degeneracy_strategy_list "NNN" \
        --counts_list "3" \
        --library_size 175835 \
        --print_interval 1000 \
        --log_output 

sleep 5

        
python3 ../top_variants.py \
        --output_dir $output_dir \
        --get_top_k_variants \
        --probability_T1 0.95 \
        --ks_list "1,10,100,1000"
import argparse
import os.path
import time
import sys
import top_variants_utils as utils


def main(args):
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    if args.get_top_k_variants:
        T1_prob= args.probability_T1
        all_ks= utils.get_ks_list(args.ks_list)
        tK_prob= utils.get_top_k_variants(T1_prob, all_ks)
        # print("Top k variants")
        # print(tK_prob)
        time_now= time.strftime("%Y-%m-%d-%H-%M-%S")
        with open(args.output_dir+"/"+time_now+'output_tk.txt', 'w') as f:
            f.write("Top k variants\n")
            f.write("probability_T1: "+str(args.probability_T1)+"\n")
            f.write("ks_list: "+args.ks_list+"\n")
            f.write(str(tK_prob))

        return

    

    #library parameters
    deg_strategy_list = utils.get_probabilities_list(args.degeneracy_strategy_list)
    counts = utils.get_counts_list(args.counts_list)
    p= utils.calculate_logits(deg_strategy_list, counts, args.chunk_size)
    n = len(p)
    L =  args.library_size

    if args.restart_from_iteration:
        current_iteration = args.current_iteration
        prob_t1_at_current_iteration = args.prob_t1_at_current_iteration
        probability_T1 = utils.calculate_probability_T1(n, L, p, args.print_interval, current_iteration, prob_t1_at_current_iteration)
    else:
        probability_T1 = utils.calculate_probability_T1(n, L, p, args.print_interval)
    
    print("prob T1")
    print(probability_T1)

    #write output to file
    time_now= time.strftime("%Y-%m-%d-%H-%M-%S")
    with open(args.output_dir+"/"+time_now+'output.txt', 'w') as f:
        f.write("prob T1\n")
        f.write("degeneracy_strategy_list: "+args.degeneracy_strategy_list+"\n")
        f.write("counts_list: "+args.counts_list+"\n")
        f.write("library_size: "+str(args.library_size)+"\n")
        f.write("chunk_size: "+str(args.chunk_size)+"\n")
        f.write( "T1 probability: "+  str(probability_T1))
    return


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, description="\n Calculate the probability of finding the top variant.")
    argparser.add_argument("--output_dir", type=str, default="output", help="Output directory")
    argparser.add_argument("--get_top_k_variants", action="store_true", help="Get top k variants")
    argparser.add_argument("--probability_T1", type=float, default=0.8371929152161488, help="Probability of finding the top variant")
    argparser.add_argument("--ks_list", type=str, default="1,10,100,1000", help="List of k values concatenated by commas, eg. 1,10,100,1000")
    argparser.add_argument("--degeneracy_strategy_list", type=str, default="NNN", help="List of degeneracy strategies concatenated by commas, eg. NNN,NNS,DKS")
    argparser.add_argument("--counts_list", type=str, default="3", help="List of counts concatenated by commas, eg. 1,2,3")
    argparser.add_argument("--library_size", type=int, default=79041, help="Library size")
    argparser.add_argument("--chunk_size", type=int, default=1000, help="Chunk size to generate the tensor probabilities")
    argparser.add_argument("--print_interval", type=int, default=100000, help="Number interval to print the iteration step")
    argparser.add_argument("--log_output", action="store_true", help="Log output")
    argparser.add_argument("--restart_from_iteration", type=int, default=None, help="Restart from iteration")
    args = argparser.parse_args()    
    if args.log_output:
        time_now= time.strftime("%Y-%m-%d-%H-%M-%S")
        sys.stdout = open(args.output_dir+"/"+time_now+'output.log', 'w')
        sys.stderr = sys.stdout
    
    main(args)  



# #library parameters
# probabilities_list = [utils.prob_NNN,utils.prob_NNN]
# counts = [2,1]

# #parameters for simulation
# p= utils.calculate_logits(probabilities_list, counts)
# n = len(p)
# L =  79041


# probability_T1 = utils.calculate_probability_T1(n, L, p,  current_iteration=7000, prob_t1_at_current_iteration=0.8371929152161488)
# probability_T1_old = utils.calculate_probability_T1_old(n, L, p)

# print("prob T1")
# print(probability_T1)
# print(probability_T1_old)

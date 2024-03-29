import itertools
import numpy as np
try:
    import cupy as cp
except ImportError:
    import numpy as cp

# Sample data
prob_NNS = cp.array([0.06250, 0.03125, 0.03125, 0.03125, 0.03125, 0.06250,
                     0.03125, 0.03125, 0.03125, 0.09375, 0.03125, 0.03125, 0.06250,
                     0.03125, 0.09375, 0.09375, 0.06250, 0.06250, 0.03125, 0.03125])
prob_NNN = cp.array([0.062500, 0.031250, 0.031250, 0.031250, 0.031250, 0.062500, 0.031250,
                     0.046875, 0.031250, 0.093750, 0.015625, 0.031250, 0.062500, 0.031250, 0.093750,
                     0.093750, 0.062500, 0.062500, 0.015625, 0.031250])
prob_DKS = cp.array([ 0.08333333,
                     0.08333333, 0.16666667,  0.08333333,
                     0.08333333, 0.08333333,
                     0.08333333, 0.08333333,  0.16666667, 0.08333333,
                     ])


def generate_combinations(n_amino_acids, n_positions,chunk_size=1000000):
    combinations_generator = itertools.product(range(n_amino_acids), repeat=n_positions)
    while True:
        chunk = list(itertools.islice(combinations_generator, chunk_size))
        if not chunk:
            break
        yield chunk

def calculate_logits(probabilities_list, counts,chunk_size=1000000):
    # Calculate the logits for all combinations
    list_tensor_probabilities = []
    for i in range(len(probabilities_list)):
        rand_strat= probabilities_list[i]
        n_amino_acids= len(probabilities_list[i])
        n_positions = counts[i]
        tensor_probabilities = cp.zeros((n_amino_acids**n_positions,), dtype=cp.float64)
        total_iterations = (n_amino_acids**n_positions) // chunk_size + 1

        for iteration, chunk in enumerate(generate_combinations(n_amino_acids, n_positions)):
            # print(f"Iteration {iteration + 1} of {total_iterations}")
            combinations_chunk = cp.array(chunk, dtype=cp.uint16)
            logits_chunk = cp.log(rand_strat[combinations_chunk])
            indices = cp.ravel_multi_index(combinations_chunk.T, (n_amino_acids,) * n_positions)
            tensor_probabilities[indices] = cp.sum(logits_chunk, axis=1)
        p = tensor_probabilities.flatten()
        list_tensor_probabilities.append(p)
            
    # Multiply p by each set of probabilities using broadcasting
    result = list_tensor_probabilities[0]
    if len(list_tensor_probabilities) == 1:
        return result
    for i in range(len(list_tensor_probabilities)-1):
        result = result[:, cp.newaxis]+list_tensor_probabilities[i+1]
        result = result.flatten()
    return result

def calculate_probability_T1(n, L, p, print_interval = 100000, current_iteration=1, prob_t1_at_current_iteration=0 ):
    p_r = np.exp(p)
    probability_T1 =0
    true_current_iteration = current_iteration
    if current_iteration > 1:
        true_current_iteration= current_iteration+1
        probability_T1 = prob_t1_at_current_iteration
    for v in range(true_current_iteration, n + 1):
        probability_T1 += (1 / n) * (1 - (1 - p_r[v - 1]) ** L)
        if v % print_interval == 0:
            print(f"Iteration {v} of {n} ({v / n:.2%} - Ac. Prob: {probability_T1})")

    return probability_T1

def calculate_probability_T1_old(n, L, p):
    p_r= np.exp(p)
    probability_T1 = 0
    for v in range(1, n+1):
        probability_T1 += (1/n) * (1 - (1 - p_r[v-1])**L)

    return probability_T1

def calculate_probability__only_first(n, L, p, last_max_T1 ):
    p_r = np.exp(p)
    probability_T1 =last_max_T1
    v=1
    probability_T1 += (1 / n) * (1 - (1 - p_r[v - 1]) ** L)
    return probability_T1

#given a string separated by commas, return a list of of probs_NNN, probs_NNS, probs_DKS

def get_probabilities_list(probabilities_string):
    probabilities_list = []
    for prob in probabilities_string.split(","):
        if prob == "NNN":
            probabilities_list.append(prob_NNN)
        elif prob == "NNS":
            probabilities_list.append(prob_NNS)
        elif prob == "DKS":
            probabilities_list.append(prob_DKS)
    return probabilities_list

#given a string separated by commas, return a list of of counts
def get_counts_list(counts_string):
    counts_list = []
    for count in counts_string.split(","):
        counts_list.append(int(count))
    return counts_list


def get_top_k_variants(T1_prob, all_ks=[1,10,100,1000]):
    tK_prob= []
    for k in all_ks:
        tK_prob.append(1- (1-T1_prob)**k)
    return tK_prob

def get_ks_list(ks_string):
    ks_list = []
    for k in ks_string.split(","):
        ks_list.append(int(k))
    return ks_list
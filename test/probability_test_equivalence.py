import os
import sys

# Get the current working directory.
cwd = os.getcwd()
# Add the parent directory to the Python path.
sys.path.append(cwd)

import numpy as np
import unittest
import top_variants_utils as utils


class TestCalculateLogits(unittest.TestCase):
    def test_prob_t1_and_t1_old(self):
        # Define your inputs and expected outputs
        #library parameters
        probabilities_list = [utils.prob_NNN,utils.prob_NNN]
        counts = [2,1]

        #parameters for simulation
        p= utils.calculate_logits(probabilities_list, counts)
        n = len(p)
        L =  79041

        # Call calculate_logits with these inputs
        result1 = utils.calculate_probability_T1(n, L, p)
        result2 = utils.calculate_probability_T1_old(n, L, p)


        # Assert that the two results are equal
        np.testing.assert_array_almost_equal(result1, result2, decimal=8)
    
    def test_equivalence2(self):
         #library parameters
        probabilities_list = [utils.prob_NNN,utils.prob_NNN]
        counts = [2,1]

        #parameters for simulation
        p= utils.calculate_logits(probabilities_list, counts)
        n = len(p)
        L =  79041
        result1 = utils.calculate_probability_T1(n, L, p,  current_iteration=7000, prob_t1_at_current_iteration=0.8371929152161488)
        result2 = utils.calculate_probability_T1(n, L, p)

        np.testing.assert_array_almost_equal(result1, result2, decimal=8)


if __name__ == '__main__':
    unittest.main()

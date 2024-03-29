
import numpy as np
import unittest
import top_variants_utils as utils

# This test checks the equivalence of the calculate_logits function's output
# for two different sets of inputs that should theoretically produce the same output.
# It sorts the results and asserts that they are almost equal up to 8 decimal places.
# This ensures that the function correctly calculates the logits regardless of the order 
# in which the probabilities and counts are provided.
class TestCalculateLogits(unittest.TestCase):
    def test_equivalence(self):
        # Define your inputs and expected outputs
        probabilities_list1 = [utils.prob_NNN, utils.prob_DKS, utils.prob_NNN]
        counts1 = [1, 1, 1]
        probabilities_list2 = [utils.prob_NNN, utils.prob_DKS]
        counts2 = [2, 1]

        # Call calculate_logits with these inputs
        result1 = utils.calculate_logits(probabilities_list1, counts1)
        result2 = utils.calculate_logits(probabilities_list2, counts2)

        # Sort the results
        result1 = np.sort(result1)
        result2 = np.sort(result2)


        # Assert that the two results are equal
        np.testing.assert_array_almost_equal(result1, result2, decimal=8)

if __name__ == '__main__':
    unittest.main()

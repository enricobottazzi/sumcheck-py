import unittest
from arithmetic import MultivariatePolynomial, UnivariatePolynomial, evaluate_multivariate, generate_combinations
from sumcheck import Prover
import random

class TestArithmetic(unittest.TestCase):

    def test_build_multivar_poly(self):
        
        # Define the multivariate polynomial f(x, y, z) = x^2 + 2xy + 3y^2 + z
        coeffs = {(2, 0, 0): 1, (1, 1, 0): 2, (0, 2, 0): 3, (0, 0, 1): 1}
        f = MultivariatePolynomial(coeffs)

        assert f.degree == 2
        assert f.num_vars == 3

        # f(0, 5, 5) = 80
        eval_values = [0, 5, 5]
        
        assert evaluate_multivariate(f, eval_values) == 80

        # turn f(x,y,z) into a univariate polynomial in x by setting y = 5, z = 5
        # g(x) = x^2 + 10x + 80
        eval_values = [5, 5]
        g = f.to_univariate(eval_values, 0)

        # check that type of g is UnivariatePolynomial
        assert type(g) == UnivariatePolynomial

        assert g.coefficients == {2: 1, 1: 10, 0: 80}

        # turn f(x,y,z) into a univariate polynomial in y by setting x = 5, z = 5
        # h(y) = 3y^2 + 10y + 30
        eval_values = [5, 5]
        h = f.to_univariate(eval_values, 1)

        assert h.coefficients == {2: 3, 1: 10, 0: 30}

    def test_sum_univariate_polynomials(self):

        g = UnivariatePolynomial({2: 1, 1: 10, 0: 80})
        h = UnivariatePolynomial({2: 2, 1: 20, 0: 160})

        assert g.add(h).coefficients == {2: 3, 1: 30, 0: 240}

    def test_generate_combinations(self):

        # # Generate all combinations of 3 variables with 2 possible values (0, 1)
        # # 000, 001, 010, 011, 100, 101, 110, 111
        assert generate_combinations(3, []) == [[0, 0, 0], [0, 0, 1], [0, 1, 0],
                                                [0, 1, 1], [1, 0, 0], [1, 0, 1],
                                                [1, 1, 0], [1, 1, 1]]
        
class TestSumcheck(unittest.TestCase):

    def test_sumcheck(self):

        # Define the multivariate polynomial f(x, y, z) = x^2 + 2xy + 3y^2 + z
        coeffs = {(2, 0, 0): 1, (1, 1, 0): 2, (0, 2, 0): 3, (0, 0, 1): 1}
        f = MultivariatePolynomial(coeffs)

        prover = Prover(f)

        # f(0, 0, 0) + f(0, 0, 1) + f(0, 1, 0) + f(0, 1, 1) + f(1, 0, 0) + f(1, 0, 1) + f(1, 1, 0) + f(1, 1, 1)
        # = 0        +    1       +    3       +    4       +     1      +    2       +    6       +  7  = 24
        sum = prover.build_sum_in_hypercube()
        assert sum == 24

        # Round 1 -> generate univariate polynomial f1(X)
        # f1(x) = (X, 0, 0) + (X, 0, 1) + (X, 1, 0)        + (X, 1, 1)
        #       = (x^2)     + (x^2 + 1) + (x^2 + 2x + 3)   + (x^2 + 2x + 4)
        #       = 4x^2 + 4x + 8
        f1 = prover.generate_univariate_poly_for_round_i()
        assert f1.coefficients == {2: 4, 1: 4, 0: 8}

        # Verifier checks that degree(f1) is less or equal than degree(f)
        assert f1.degree <= f.degree

        # Verifier checks that f1(0) + f1(1) = sum
        assert f1.evaluate(0) + f1.evaluate(1) == sum

        # Verfiier generates a random challenge 
        r1 = random.randint(0, 1000)

        # Prover receives the challenge 
        prover.r.append(r1)

        # Round 2 -> generate univariate polynomial f2(X)
        # f2(X)= (r1, X, 0)               + (r1, X, 1)
        #      = (r1^2 + 2r1X + 3X^2 + 0) + (r1^2 + 2r1X + 3X^2 + 1)\
        #      = 6X^2 + 4r1X + 2r1^2 + 1
        f2 = prover.generate_univariate_poly_for_round_i()
        assert f2.coefficients == {2: 6, 1: 4*r1, 0: 2*r1**2 + 1}

        # Verifier checks that degree(f2) is less or equal than degree(f)
        assert f2.degree <= f.degree

        # Verifier checks that f2(0) + f2(1) = f1(r1)
        assert f2.evaluate(0) + f2.evaluate(1) == f1.evaluate(r1)

        # Verfiier generates a random challenge 
        r2 = random.randint(0, 1000)

        # Prover receives the challenge 
        prover.r.append(r2)

        # Round 3 -> generate univariate polynomial f3(X)
        # f3(X) = (r1, r2, X)
        #       = r1^2 + 2r1r2 + 3r2^2 + X
        #       = X + 2r1r2 + 3r2^2 + r1^2

        f3 = prover.generate_univariate_poly_for_round_i()
        assert f3.coefficients == {2: 0, 1: 1, 0: 3*r2**2 + r1**2 + 2*r1*r2}

        # Verifier checks that degree(f3) is less or equal than degree(f)
        assert f3.degree <= f.degree

        # Verifier checks that f3(0) + f3(1) = f2(r2)
        assert f3.evaluate(0) + f3.evaluate(1) == f2.evaluate(r2)

        # Verfiier generates a random challenge (this is the final challenge)
        r3 = random.randint(0, 1000)

        prover.r.append(r3)

        # FINAL CHECK
        # The verifier evaluates f(r1, r2, r3) and confirms that it equals f3(r3)
        assert evaluate_multivariate(f, prover.r) == f3.evaluate(r3)

if __name__ == "__main__":
    unittest.main()
from arithmetic import MultivariatePolynomial, UnivariatePolynomial, generate_combinations, evaluate_multivariate

class Prover:
    def __init__(self, poly: MultivariatePolynomial):
        """
        Initialize the prover for a sumcheck protocol with a multivariate polynomial.
        
        Attributes:
            poly (MultivariatePolynomial): The polynomial that the prover is trying to prove knowledge of a sum in the hypercube space
                                
        Example usage:
            f = MultivariatePolynomial({(2, 0, 0): 1, (1, 1, 0): 2, (0, 2, 0): 3, (0, 0, 1): 1})
            prover = Prover(f)
        """
        self.poly = poly
        self.r = []

    def build_sum_in_hypercube(self):
        """
        Build the sum of the polynomial in the hypercube space. For example for the multi-variate polynomial f(x, y, z)
        sum = (0, 0, 0) + (0, 0, 1) + (0, 1, 0) + (0, 1, 1) + (1, 0, 0) + (1, 0, 1) + (1, 1, 0) + (1, 1, 1) where each tuple is an evaluation of the polynomial
        """

        combos = generate_combinations(self.poly.num_vars)

        sum = 0

        for combo in combos:
            sum += evaluate_multivariate(self.poly, combo)

        return sum

    def generate_univariate_poly_for_round_i(self):
        """
        Generate the univariate polynomial for round i of the sumcheck protocol.
        For example for the multi-variate polynomial f(x, y, z)
        At round 1 the univariate polynomial is f1(X) = f(X, 0, 0) + f(X, 0, 1) + f(X, 1, 0) + f(X, 1, 1)
        At round 2 the univariate polynomial is f2(X) = f(r1, X, 0) + f(r1, X, 1) where r1 is the challenge from round 1
        """

        cum_univariate = UnivariatePolynomial({2: 0, 1: 0, 0: 0})

        combos = generate_combinations(self.poly.num_vars - 1 - len(self.r))

        for combo in combos:
            eval_values = self.r + combo
            g = self.poly.to_univariate(eval_values, len(self.r))
            cum_univariate = g.add(cum_univariate)
      
        return cum_univariate

        
                
            



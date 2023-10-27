from collections import OrderedDict

class MultivariatePolynomial:

    """
    Represents a multivariate polynomial in n variables x1, x2, ..., xn.
    
    Attributes:
        coefficients (dict): Dictionary mapping tuples of integers to coefficients.
                             Each tuple represents the powers of variables in a term,
                             and the value represents the coefficient of that term.
                             For example, {(2, 0, 0): 1, (1, 1, 0): 2, ...} 
                             represents the polynomial x^2 + 2xy + ...
                             
    Example usage:
        f = MultivariatePolynomial({(2, 0, 0): 1, (1, 1, 0): 2, (0, 2, 0): 3})
    """

    def __init__(self, coefficients):
        self.coefficients = coefficients
        self.degree = self.degree()
        self.num_vars = len(list(self.coefficients.keys())[0])

    def degree(self):
        max_degree = -1  # Initialize to -1 as we have not seen any term yet
        for powers, coeff in self.coefficients.items():
            if coeff != 0:  # Ignoring terms with zero coefficients
                current_degree = sum(powers)
                max_degree = max(max_degree, current_degree)
        return max_degree


    def to_univariate(self, eval_values, keep_var_index):

        """
        Converts the multivariate polynomial to a univariate polynomial by 
        evaluating all variables except the one at `keep_var_index`.
        
        Args:
            eval_values (list): List of numerical values for each variable.
            keep_var_index (int): The index of the variable to keep.
            
        Returns:
            UnivariatePolynomial: A new UnivariatePolynomial object polynomial.
        """

        # Initialize the result polynomial as an empty OrderedDict
        g = OrderedDict()

        # Sort the multivariate terms by the power of the variable we wish to keep, in descending order
        sorted_terms = sorted(self.coefficients.items(), key=lambda x: x[0][keep_var_index], reverse=True)

        for powers, coeff in sorted_terms:
            new_power = powers[keep_var_index]
            eval_powers = [p for i, p in enumerate(powers) if i != keep_var_index]
            
            term_value = evaluate_multivariate(MultivariatePolynomial({tuple(eval_powers): coeff}), eval_values)
            
            if new_power in g:
                g[new_power] += term_value
            else:
                g[new_power] = term_value

        # Construct and return a new UnivariatePolynomial object
        return UnivariatePolynomial(g)


def evaluate_multivariate(multivariate_poly: MultivariatePolynomial, eval_values) :

    """
    Evaluate the polynomial at specified points.

    Args:
        multivariate_poly (MultivariatePolynomial): The polynomial to evaluate.
        eval_values (list): List of numerical values for each variable.

    Returns:
        The value of the polynomial at the specified points.
    """

    result = 0
    for powers, coeff in multivariate_poly.coefficients.items():
        term_value = coeff
        for var_power, var_value in zip(powers, eval_values):
            term_value *= (var_value ** var_power)
        result += term_value
    return result

def generate_combinations(n, prefix=None, result=None):
    if prefix is None:
        prefix = []
    if result is None:
        result = []
    if len(prefix) == n:
        result.append(prefix.copy())  # Copy prefix so that the appended list is independent
        return result
    for bit in [0, 1]:
        new_prefix = prefix + [bit]
        generate_combinations(n, new_prefix, result)
    
    return result

class UnivariatePolynomial:

    """
    Represents a univariate polynomial in one variable x.
    
    Attributes:
        coefficients (dict): Dictionary mapping integers to coefficients.
                             Each integer represents the power of the variable in a term,
                             and the value represents the coefficient of that term.
                             For example, {2: 1, 1: -3, 0: 1} represents the polynomial x^2 - 3x + 1.
                             
    Example usage:
        f = UnivariatePolynomial({2: 1, 1: -3, 0: 1})
    """

    def __init__(self, coefficients):
        self.coefficients = coefficients
        self.degree = self.degree()

    def degree(self):
        max_degree = -1  # Initialize to -1 as we have not seen any term yet
        for power, coeff in self.coefficients.items():
            if coeff != 0:  # Ignoring terms with zero coefficients
                max_degree = max(max_degree, power)
        return max_degree

    def add(self, other):
        """
        Add another UnivariatePolynomial to this one.
        
        Args:
            other (UnivariatePolynomial): The polynomial to add to the current instance.
            
        Returns:
            UnivariatePolynomial: New UnivariatePolynomial representing the sum.
        """
        # Initialize the result polynomial as an empty dictionary
        sum_poly = {}
        
        # Add terms from the current polynomial
        for power, coeff in self.coefficients.items():
            sum_poly[power] = coeff
        
        # Add terms from the other polynomial
        for power, coeff in other.coefficients.items():
            if power in sum_poly:
                sum_poly[power] += coeff
            else:
                sum_poly[power] = coeff
        
        return UnivariatePolynomial(sum_poly)
    
    def evaluate(self, x):
        """
        Evaluate the polynomial at a specified point.
        
        Args:
            x (int): Point to evaluate the polynomial at.
            
        Returns:
            int: The value of the polynomial at the specified point.
        """
        result = 0
        for power, coeff in self.coefficients.items():
            result += coeff * (x ** power)
        return result
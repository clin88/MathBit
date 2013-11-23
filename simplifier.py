from collections import OrderedDict
from operators import *
from operators import Number


class Simplifier(object):
    def __init__(self, output_delegate):
        self._output = output_delegate

    def _report_step(self):
        self._output.add_step(self._expression)

    def simplify(self, expr):
        """
            Simplifies an expression. Handles the following cases:

            1. Combines like terms.
        """
        assert isinstance(expr, Expr)
        self._expression = expr
        self._simplify_expr(self._expression.child)
        return self._expression

    def _simplify_expr(self, node):
        if isinstance(node, Mult):
            self._simplify_mult(node)
        elif isinstance(node, Plus):
            self._simplify_addition(node)

        return node


    def _simplify_mult(self, node):
        """
            Takes the terms in an expression, seperates numerators and denominators, and simplifies the result.

            e.g. 3 * x / 4 * y = 3xy / 4
        """
        numerator = Mult()
        denominator = Mult()

        for child in node.children:
            if isinstance(child, Operator):
                self._simplify_expr(child)

            if isinstance(child, Fraction):
                numerator.add_children(child.numerator)
                denominator.add_children(child.denominator)
            else:
                numerator.add_children(child)

        if not denominator.children:
            self._simplify_product(node)
        else:
            # TODO: Simplify this fraction
            node.replace_self(Fraction(numerator, denominator))
            self._report_step()

            self._simplify_product(node.numerator)
            self._simplify_product(node.denominator)



    def _simplify_product(self, node):
        """
            Simplifies a Mult() containing no fractions.
        """
        factors = OrderedDict()
        constant = 1
        # iterate through children recording the number of times each factor appears
        while node.children:
            child = node.pop_child(0)

            # remove nested multiplication. e.g. 2 * (x * 3) -> 2 * x * 3
            if isinstance(child, Mult):
                node.add_children(*child.children)
            elif isinstance(child, Number):
                constant *= child
            elif isinstance(child, Exp):
                factors[child.base] = factors.get(child.base, 0) + child.exponent
            else:
                factors[child] = factors.get(child, 0) + 1

        # reconstruct the product, grouping like factors using powers
        if constant != 1:
            node.insert_child(0, constant)
        for factor, power in factors.iteritems():
            node.add_children(Exp(factor, power))                       # TODO: Simplify on the fly, this should also simplify exponents of 1

        # TODO: Report step

        # if after simplification, node is only one item, carry it out
        if len(node.children) == 1:
            node.replace_self(node.children[0])


    def _simplify_addition(self, node):
        """
            Plus and Mult: c + c + xy + xy -> 2c + 2xy
            Exponents too: c^2 + c^2 = 2c^2
        """
        constant = 0
        terms = OrderedDict()
        while node.children:
            child = node.pop_child(0)
            self._simplify_expr(child)

            if isinstance(child, Plus):
                node.add_children(*child.children)
            elif isinstance(child, Number):
                constant += child
            elif isinstance(child, Mult):
                # we assume that this is in simplified form, so the constant factor comes first or not at all
                if isinstance(child.children[0], Number):
                    n = child.pop_child(0)
                else:
                    n = 1

                terms[child] = terms.get(child, 0) + n
            # TODO: Support fractions
            else:
                terms[child] = terms.get(child, 0) + 1

        for term, count in terms.iteritems():
            node.add_children(self._simplify_expr(Mult(count, term)))

        if constant:
            node.add_children(constant)

        if len(node.children) == 1:
            node.replace_self(node.children[0])


        # TODO: Use numbers module for numbers.
        # TODO: Subclass children list and override inplace change methods for simpler syntax and better safety

    #def _simplify_fraction(self, node):
    #    self._simplify_expr(node.numerator)
    #    self._simplify_expr(node.denominator)
    #
    #    numerator = node.numerator
    #    denominator = node.denominator
    #    if isinstance(numerator, Fraction):
    #        if isinstance(denominator, Fraction):
    #            replacement = Mult(numerator, Fraction(denominator.denominator, denominator.numerator))
    #            node.replace_self(replacement)
    #            # TODO: report step
    #            self._simplify_expr(node)
    #
    #        else:
    #            replacement = Mult(numerator, Fraction(1, denominator))
    #            node.replace_self(replacement)
    #            self._simplify_expr(node)
    #
    #    elif isinstance(numerator, Exp):
    #        if isinstance(denominator, Exp):
    #            if numerator.base == denominator.base:
    #                replacement = Exp(numerator.base, numerator.exponent - denominator.exponent)
    #        elif isinstance(denominator, Mult):
    #            pass
    #
    #
    #    elif isinstance(numerator, Mult):


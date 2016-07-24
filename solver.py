#!/usr/bin/env python

from __future__ import division

import itertools
import re

'''
    Given an equation such as '1_3_4_6=24' using any combination of the operators [\, *, -, +]
    in the "_" slots, find how many solutions there are, and how many guesses you'd need to find them all.
'''


class Solver:
    lhs_args = []
    rhs = None
    _operators_ = ['/', '*', '+', '-']
    guesses_required = 0

    def __init__(self, equation):
        """
        :type equation: str
        """
        r = re.match('^(\d+)_(\d+)_(\d+)_(\d+)=(\d+)$', equation)
        if r is None:
            raise Exception('Invalid String')

        self.lhs_args = [int(g) for g in r.groups()[:-1]]
        self.rhs = float(r.groups()[-1])

    def solve(self):
        for nums in itertools.permutations(self.lhs_args):
            for opcombo in itertools.product(self._operators_, repeat=4):
                self._gen_lhs_(nums, opcombo, lambda x: self._test_(x))

    def _gen_lhs_(self, nums, opcombo, func):
        """
        :type nums: list
        :type opcombo: list
        """

        # interleave the lists
        result = list(nums) + list(opcombo)
        result[0::2] = nums
        result[1::2] = opcombo
        result.pop()  # we wanted the permutations above, but don't want the final operator
        func(result)
        self._check_paren_alts_(result, lambda x: self._test_(x))

    def _check_paren_alts_(self, equation, func):
        """
        :type equation: list
        """
        '''
            We only care about the windowing of
            <operand> <operator> <operand> <operator>
            so exclude the later short results in the window
        '''
        i = 0
        while i < len(equation) - 3:
            window = equation[0 + i:4 + i]
            ops_in_window = [x for x in filter(lambda y: y in self._operators_, window)]
            ordered_operators = [x for x in filter(lambda y: y in window, self._operators_)]
            if len(ordered_operators) > 1 and ordered_operators != ops_in_window:
                for j in [0, 2]:
                    temp = list(equation)
                    pos = equation.index(ordered_operators[1])
                    temp.insert(pos - 1, '(')
                    temp.insert(pos + 3 + j, ')')
                    func(temp)

            i += 1

    def _test_(self, equation):
        """
        :type equation: list
        """
        equation = ' '.join(map(str, equation))
        self.guesses_required += 1
        try:
            if float(eval(equation)) == self.rhs:
                print(equation)
        except:
            pass


s = Solver('1_3_4_6=24')
s.solve()
print("Number of guesses required: %d" % s.guesses_required)

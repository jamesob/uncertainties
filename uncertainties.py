#!/usr/bin/env python

# by jamesob
# because I love physics lab

import math

class UncertainVariable(object):
    """A class defining a variable with associated uncertainty stored as a
    physical quantity and a percentage. Uncertainties are automatically
    calculated and maintained as the variable is operated on.
    
    Values must be set before associated uncertainties are.

    >>> x = UncertainVariable(44.8, 0.2)
    >>> t = UncertainVariable(3.21, 0.02)
    >>> res = x / t**2
    >>> res.val
    4.3477838918488754
    >>> res.uncert
    0.057549919541000298
    >>> res.uncertPerc
    1.3236609954071901
    """

    def __init__(self, val=1., uncert=1.):
        self.val         = val
        self._uncert     = uncert
        self._uncertPerc = 100.0 * (uncert / val)

    def getUnc(self):
        return self._uncert

    def setUnc(self, unc):
        self._uncert = unc
        self._uncertPerc = 100.0 * (unc / self.val)

    uncert = property(getUnc, setUnc, doc="Uncertainty in units.")

    def getPerc(self):
        return self._uncertPerc

    def setPerc(self, uncPerc):
        self._uncertPerc = uncPerc
        self._uncert     = (uncPerc * self.val) / 100.0

    uncertPerc = property(getPerc, setPerc, doc="Uncertainty percentage.")
    
    def _addAndSub(a, b, op):
        """Not to be used outside of class definition. Encapsulates similarities
        between addition and subtraction."""

        if isinstance(b, UncertainVariable):
            a.val = op(a.val, b.val)
            a.setUnc(math.sqrt(a.uncert**2 + b.uncert**2))
        else:
            a.val = op(a.val, b)
            a.setUnc(a.uncert)
        return a

    def _multAndDiv(a, b, op):
        """Not to be used outside of class definition. Encapsulates similarities
        between mult. and div."""

        if isinstance(b, UncertainVariable):
            a.val = op(a.val, b.val)
            a.setPerc(math.sqrt(a.uncertPerc**2 + b.uncertPerc**2))
        else:
            a.val = op(a.val, b)
            a.setUnc(op(a.uncert, b))
        return a

    def __add__(self, other):
        """Overloads the + operator for this object."""
        return self._addAndSub(other, lambda x, y: x + y)
        
    def __sub__(self, other):
        """Overloads the - operator for this object."""
        return self._addAndSub(other, lambda x, y: x - y)

    def __mul__(self, other):
        """Overloads multiplication operator."""
        return self._multAndDiv(other, lambda x, y: x * y)

    def __div__(self, other):
        """Overloads division operator."""
        return self._multAndDiv(other, lambda x, y: x / y)

    def __pow__(self, other):
        """Overloads the exponent operator."""
        self.val         = self.val**other
        self.setPerc(self.uncertPerc * other)
        return self

    def specialFunction(self, fnc):
        """For special functions, e.g. sin, log, exp."""
        plusUnc  = self.val + self.unc
        minUnc   = self.val - self.unc
        upperVal = fnc(plusUnc) - fnc(self.val)
        lowerVal = fnc(minUnc) - fnc(self.val)

        self.val    = fnc(self.val)
        self.uncert = (upperVal + lowerVal) / 2.0
        return self

if __name__ == '__main__':
    import doctest
    doctest.testmod()


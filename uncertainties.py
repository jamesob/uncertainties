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

    >>> mu = UncertainVariable(0.004, 0.2 / 1000)
    >>> L  = UncertainVariable(0.6, 0.5 / 100) 
    >>> res = 4 * mu
    >>> res2 = L ** 2
    >>> yores = res * res2
    >>> foores = 4 * mu * L**2
    >>> foores.val == yores.val
    True
    >>> foores.uncert == yores.uncert
    True
    >>> foores.uncertPerc == yores.uncertPerc
    True
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

        newVar = UncertainVariable()
        if isinstance(b, UncertainVariable):
            newVar.val = op(a.val, b.val)
            newVar.setUnc(math.sqrt(a.uncert**2 + b.uncert**2))
        else:
            newVar.val = op(a.val, b)
            newVar.setUnc(a.uncert)
        return newVar

    def _multAndDiv(a, b, op):
        """Not to be used outside of class definition. Encapsulates similarities
        between mult. and div."""

        newVar = UncertainVariable()
        if isinstance(b, UncertainVariable):
            newVar.val = op(a.val, b.val)
            newVar.setPerc(math.sqrt(a.uncertPerc**2 + b.uncertPerc**2))
        else:
            newVar.val = op(a.val, b)
            newVar.setUnc(op(a.uncert, b))
        return newVar

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
        newVar = UncertainVariable()
        newVar.val = self.val**other
        newVar.setPerc(self.uncertPerc * other)
        return newVar

    def __radd__(self, other):
        return self.__add__(other)

    def __rsub__(self, other):
        return self.__sub__(other)

    def __rdiv__(self, other):
        return self.__div__(other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __rpow__(self, other):
        return self.__pow__(other)

    def specialFunction(self, fnc):
        """For special functions, e.g. sin, log, exp."""
        newVar   = UncertainVariable()
        plusUnc  = self.val + self.unc
        minUnc   = self.val - self.unc
        upperVal = fnc(plusUnc) - fnc(self.val)
        lowerVal = fnc(minUnc) - fnc(self.val)

        newVar.val = fnc(self.val)
        newVar.setUnc((upperVal + lowerVal) / 2.0)
        return self

if __name__ == '__main__':
    import doctest
    doctest.testmod()


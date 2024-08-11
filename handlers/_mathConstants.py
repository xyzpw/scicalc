import math
import cmath
from handlers._symbols import *
import statistics
import sympy
import scipy
import numpy

__all__ = [
    "c",
    "g",
    "G",
    "pi",
    "e",
    "h",
    "kb",
    "phi",
    "NA",
    "ke",
    "e0",
    "R",
    "log10",
    "ln",
    "log2",
    "cbrt",
    "sqrt",
    "constants",
    "exp",
    "erf",
    "erfc",
    "floor",
    "ceil",
    "median",
    "mode",
    "z2p",
    "p2z",
    "fact",
    "factorial",
    "normaltest",
    "product",
    "prod",
    "gmean",
    "pstdev",
]

c = 299792458
g = 9.80665
G = 6.67430 * 10**-11
pi = float(math.pi)
e = float(math.e)
h = 6.62607015e-34
kb = 1.380649e-23
phi = (1 + math.sqrt(5)) / 2
NA = 6.02214076 * 10**23
ke = 8.9875517923e+9
e0 = 8.8541878128e-12
R = 8.31446261815324

log10 = math.log10
ln = math.log
log2 = math.log2
cbrt = lambda n: n**(1/3)
def sqrt(num):
    """Returns the square root of a number."""
    result = None
    if num > 0:
        result = math.sqrt(num)
        result = int(result) if result.is_integer() else result
    elif num < 0:
        result = cmath.sqrt(num)
    elif num == 0:
        result = 0
    return result

constants = {
    "c": f"Speed of light {c:,} m/s",
    "g": f"Standard gravity {g} m/s{mathSymbols['squared']}",
    "G": f"Gravitational constant {G} N{mathSymbols['cdot']}m{mathSymbols['squared']}{mathSymbols['cdot']}kg{mathSymbols['negative']}{mathSymbols['squared']}",
    "h": f"Planck constant {h} J{mathSymbols['cdot']}Hz{mathSymbols['negative']}{mathSymbols['first']}",
    "kb": f"Boltzmann constant {kb} J{mathSymbols['cdot']}K{mathSymbols['negative']}{mathSymbols['first']}",
    "phi": f"Golden ratio {phi}",
    "NA": f"Avogadro constant {NA} mol{mathSymbols['negative']}{mathSymbols['first']}",
    "ke": f"Coulomb constant {ke} N{mathSymbols['cdot']}m{mathSymbols['squared']}{mathSymbols['cdot']}C{mathSymbols['negative']}{mathSymbols['squared']}",
    "e0": f"Electric constant {e0} F{mathSymbols['cdot']}m{mathSymbols['negative']}{mathSymbols['first']}",
    "R": f"Gas constant {R} J{mathSymbols['cdot']}K{mathSymbols['negative']}{mathSymbols['first']}{mathSymbols['cdot']}mol{mathSymbols['negative']}{mathSymbols['first']}",
}

exp = math.exp
erf = math.erf
erfc = math.erfc
floor = math.floor
ceil = math.ceil
median = statistics.median
mode = statistics.multimode
z2p = scipy.stats.norm.cdf
p2z = scipy.stats.norm.ppf
fact, factorial = math.factorial, math.factorial
normaltest = scipy.stats.normaltest
product, prod = numpy.prod, numpy.prod
gmean = scipy.stats.gmean
pstdev = statistics.pstdev


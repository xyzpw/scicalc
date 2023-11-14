#!/usr/bin/env python3

import prompt_toolkit
import math
import os
import re
import statistics
import scipy
import warnings
import argparse
import sympy
import decimal
import sys

sys.set_int_max_str_digits(0) # allowing very large numbers

sympy.init_printing(pretty_print=True, use_unicode=True)

uiSession = prompt_toolkit.PromptSession()
parse = argparse.ArgumentParser()
parse.add_argument("-e", help="Equation to solve", type=str)
args = parse.parse_args()

var_args = vars(args)

warnings.filterwarnings("ignore")

exitAttempts = 0

history = []

class Symbols:
    degree = '\u00b0'
    plus_minus = '\u00b1'
    squared = '\u00b2'
    cubed = '\u00b3'
    cdot = '\u00b7'
    first = '\u00b9'
    negative = '\u207b'
    phi = '\u03d5'
    pi = '\u03c0'
    divide = '\u00f7'
    class Radicals:
        sqrt = '\u221a'
        cbrt = '\u221b'
    class Fractions:
        fourth = '\u00bc'
        half = '\u00bd'
        quarter3 = '\u00be'

# constants
c = 299792458
g = 9.80665
G = 6.67430 * 10**-11
pi = math.pi
e = math.e
h = 6.62607015e-34
k = 1.380649e-23
phi = (1 + math.sqrt(5)) / 2

constants = {"c": f"Speed of light {c:,} m/s",
    "g": f"Standard gravity {g} m/s{Symbols.squared}",
    "G": f"Gravitational constant {G} N{Symbols.cdot}m{Symbols.squared}/kg{Symbols.squared}",
    "h": f"Planck's constant {h} J/Hz",
    "k": f"Boltzmann constant {k} J/K",
    "phi": f"Golden ratio {phi}",
}

# functions
log10 = math.log10
ln = math.log
log2 = math.log2
cbrt = math.cbrt
sqrt = math.sqrt
exp = math.exp
erf = math.erf
erfc = math.erfc
floor = math.floor
ceil = math.ceil
mean, average, avg = statistics.mean, statistics.mean, statistics.mean
median = statistics.median
mode = statistics.multimode
z2p = scipy.stats.norm.cdf
p2z = scipy.stats.norm.ppf
fact, factorial = math.factorial, math.factorial
normaltest = scipy.stats.normaltest
product, prod = scipy.prod, scipy.prod
gmean = scipy.stats.gmean
pstdev = statistics.pstdev
ptp = scipy.ptp

def isNumber(value):
    if str(value).isnumeric():
        return True
    else:
        try:
            value = float(value)
            return True
        except:
            return False


def useSymbols(equation):
    equation = str(equation)
    replacements = {
        "\*": Symbols.cdot,
        "sqrt": Symbols.Radicals.sqrt,
        "cbrt": Symbols.Radicals.cbrt,
        "\(1/2\)": Symbols.Fractions.half,
        "\(1/4\)": Symbols.Fractions.fourth,
        "\(3/4\)": Symbols.Fractions.quarter3,
        "phi": Symbols.phi,
        "pi": Symbols.pi,
        "/": Symbols.divide,
    }
    for sym, val in replacements.items():
        equation = re.sub(sym, val, equation)
    return equation

def addToHistory(equation, result, includeAll=False):
    global history
    if isNumber(result) and isinstance(result, (int, float)):
        # remove last equation from history if the max. limit is reached
        if len(history) >= 40:
            history.pop(0)
        if result >= 1e18 and result < sys.float_info.max:
            appendText = f"{useSymbols(equation)} = {result:e}"
            if appendText in history:
                history.remove(appendText)
            history.append(appendText)
        else:
            appendText = f"{useSymbols(equation)} = {result:,}"
            if appendText in history:
                history.remove(appendText)
            history.append(appendText)
    elif isinstance(result, list):
        appendText = f"{useSymbols(equation)} = {result}"
        if appendText in history:
            history.remove(appendText)
        history.append(appendText)
    elif includeAll:
        appendText = f"{equation} = {result}"
        if appendText in history:
            history.remove(appendText)
        history.append(appendText)

def fixUI(userValue):
    global history
    match userValue.lower():
        case "history" | "hist":
            print(*history, sep='\n')
            return None
        case "clear history" | "clear hist":
            history = []
            return None
        case "constant" | "constants" | "const":
            for key, value in constants.items():
                print(f"{key} => {value}")
            return None
        case "exit":
            exit()
    userValue = re.sub('\^', "**", userValue)
    return userValue

# more functions
def deg2rad(deg):
    return math.pi / 180 * deg

def rad2deg(rad):
    return 180 / math.pi * rad

def log(base, n): return math.log10(n) / math.log10(base)

def root(nth, n): return pow(n, 1/nth)

def roundup(n, prec=0):
    """
    Round 5 up
    roundup(2.5, prec=0) = 3
    """
    n = n * 10**prec
    result = decimal.Decimal(n).quantize(0, decimal.ROUND_HALF_UP)
    result /= 10**prec
    return float(result)

def rounddown(n, prec=0):
    """
    Round 5 down
    rounddown(2.5, prec=0) = 2
    """
    n = n * 10**prec
    result = decimal.Decimal(n).quantize(0, decimal.ROUND_HALF_DOWN)
    result /= 10**prec
    return (float(result))

def nCr(n, r): return math.factorial(n) // ( math.factorial(r) * math.factorial(n - r) )

def nPr(n, r): return math.factorial(n) // math.factorial(n - r)

def binomial(p, n, x):
    """
    Usage: binomial(p, n, x)
    p => probability of success
    n => number of trials
    x => number of successes
    """
    numberOfCombinations = nCr(n, x)
    q = 1 - p
    binomialProbability = numberOfCombinations * p**x * q**(n - x)
    return binomialProbability

def integrate(f, lower=None, upper=None, pretty=True):
    """
    Uses sympy.integrate with custom options
    Note: When integrating without limits, you add the '+ C' at the end.
    """
    if lower != None and upper != None:
        result = sympy.integrate(f, ('x', lower, upper))
        newEquation = f"integrate({f}, lower={lower}, upper={upper})"
        addToHistory(newEquation, str(result), includeAll=True)
        if pretty:
            return sympy.pprint(result)
        else:
            return result
    if lower == None and upper == None:
        result = sympy.integrate(f)
        newEquation = f"integrate({f})"
        addToHistory(newEquation, str(result), includeAll=True)
        if pretty:
            return sympy.pprint(result)
        else:
            return result
    return "Error"
def integral(f, pretty=True):
    result = sympy.Integral(f)
    newEquation = f"integral({f})"
    addToHistory(newEquation, str(result), includeAll=True)
    if pretty:
        return sympy.pprint(result)
    elif not pretty:
        return result
    return "Error"

def lim(f, x):
    result = float( sympy.limit(f, 'x', x) )
    return result

def Lim(f, x, pretty=True):
    if pretty:
        result = sympy.pprint(sympy.Limit(f, 'x', x))
    else:
        result = sympy.Limit(f, 'x', x)
    return result

def trunc(n, p=0):
    if n == 0:
        return 0
    elif n > 0:
        return math.floor(n * 10**p) / 10**p
    elif n < 0:
        return math.ceil(n * 10**p) / 10**p
    return None

def zscore(score, mean, sd):
    """
    zscore(score, mean, sd)
    """
    return ((score - mean) / sd)

def z2pRange(z1, z2):
    """
    Percentile between two Z-scores
    z2pRange(z1, z2)
    z1 is the lower end and z2 is the upper end
    """
    p = scipy.stats.norm.cdf(z2) - scipy.stats.norm.cdf(z1)
    return p

def p2zRange(p1, p2):
    """
    Z-score between two percentiles
    p2zRange(p1, p2)
    p1 is the lower end and p2 is the upper end
    """
    z = scipy.stats.norm.ppf(p2) - scipy.stats.norm.ppf(p1)
    return z

def uncertainty(numberSet):
    """
    Uncertainty of a number array (range over 2)
    Note: Uncertainty is usually rounded to 1 significant figure
    uncertainty(numSet)
    """
    numberSetRange = max(numberSet) - min(numberSet)
    return numberSetRange / 2

def distance(n, unit1, unit2):
    """
        Convert units, e.g. distance(1, 'm', 'ft') ~ 3.28
        pm => Picometers
        nm => Nanometers
        um => Micrometers
        mm => Millimeters
        cm => Centimeters
        dm => Decimeters
        km => Kilometers
        ly => Light years
        in => inches
        ft => feet
        yd => yards
        mi => miles
        au => astronomical unit
        pc = parsec
        planck => planck length
    """
    units = {
        "m": 1,
        "pm": 1/1e12,
        "nm": 1/1e9,
        "um": 1/1e6,
        "mm": 1/1000,
        "cm": 1/100,
        "dm": 1/10,
        "km": 1000,
        "ly": 299792458 * (60 * 60 * 24 * 365.25), # we use 365.25 days for a year because there is a leap year every 4 years
        "in": 0.3048/12,
        "ft": 0.3048,
        "yd": 0.3048*3,
        "mi": 0.3048*5280,
        "au": 149597870700,
        "pc": (648000 / math.pi) * 149597870700,
        "planck": 1.616255e-35,
    }
    multiplier = units.get(unit1) # multiply by this to get meters
    n_meters = n * multiplier
    return n_meters / units.get(unit2)

def mass(n, unit1, unit2):
    """
        Convert units, e.g. mass(1, 'kg', 'lb') ~ 2.204622
        kg => kilograms
        ug => micrograms
        mg => milligrams
        g => grams
        t => metric ton
        gr => grain
        oz => ounce
        lb => pound
        st => stone
        ton => US ton
        planck => planck mass
    """
    units = {
        "kg": 1,
        "ug": 1/1e9,
        "mg": 1/1e6,
        "g": 1/1e3,
        "t": 1000,
        "gr": 64.79891/1e6,
        "oz": 0.45359237/16,
        "lb": 0.45359237,
        "st": 6.35029318,
        "ton": 907.18474,
        "planck": 2.176434e-8,
    }
    multiplier = units.get(unit1) # multiply by this to get kilograms
    n_kg = n * multiplier
    return n_kg / units.get(unit2)

def time(n, unit1, unit2):
    """
    Convert time e.g. time(1, 'min', 's') = 60
    us => microsecond
    ms => millisecond
    min => minute
    h => hour
    d => days
    wk => weeks
    a => julian year
    """
    units = {
        "s": 1,
        "us": 1/1e6,
        "ms": 1/1e3,
        "min": 60,
        "h": 3600,
        "d": 86400,
        "wk": 86400*7,
        "a": 365.25*86400,
    }
    multiplier = units.get(unit1) # multiply by this to get seconds
    n_s = n * multiplier
    return n_s / units.get(unit2)

def volume(n, unit1, unit2):
    """
    Convert volume e.g. volume(1, 'bbl', 'gal') = 42
    l => liter
    gtt => drop
    ml => milliliters
    tsp => metric teaspoon
    tbsp => metric tablespoon
    imp_floz => imperial fluid ounce
    imp_qt => imperial quart
    floz => US fluid ounce
    c => US cup
    pt => US pint
    imp_pt => imperial pint
    qt => US quart
    gal => US gallon
    imp_gal => imperial gallon
    bbl => oil barrel
    """
    units = {
        "l": 1,
        "gtt": 0.00005,
        "ml": 0.001,
        "tsp": 0.005,
        "tbsp": 0.015,
        "imp_floz": 0.0284130625,
        "floz": 0.0295735295625,
        "c": 0.2365882365,
        "pt": 0.473176473,
        "imp_pt": 0.56826125,
        "qt": 0.946352946,
        "imp_qt": 1.1365225,
        "gal": 3.785411784,
        "imp_gal": 4.54609,
        "bbl": 158.98729492799998,
    }
    multiplier = units.get(unit1) # multiply by this to get liters
    n_l = n * multiplier
    return n_l / units.get(unit2)

def quantile(numberSet, p, method='weibull'):
    return scipy.quantile(numberSet, p, method=method)

def score2p(numberSet, score, method='weak'):
    return scipy.stats.percentileofscore(numberSet, score, kind=method) / 100

def outliers(numberSet):
    outlierSet = []
    q1 = scipy.quantile(numberSet, .25, method='weibull')
    q3 = scipy.quantile(numberSet, .75, method='weibull')
    iqr = q3 - q1
    lowerFence = q1 - 1.5 * iqr
    higherFence = q3 + 1.5 * iqr
    for num in numberSet:
        if num < lowerFence or num > higherFence:
            outlierSet.append(num)
    return outlierSet

def IQR(numberSet):
    q1 = scipy.quantile(numberSet, .25, method='weibull')
    q3 = scipy.quantile(numberSet, .75, method='weibull')
    iqr = q3 - q1
    return iqr

def lowerfence(numberSet):
    q1 = scipy.quantile(numberSet, .25, method='weibull')
    q3 = scipy.quantile(numberSet, .75, method='weibull')
    iqr = q3 - q1
    return q1 - 1.5 * iqr

def upperfence(numberSet):
    q1 = scipy.quantile(numberSet, .25, method='weibull')
    q3 = scipy.quantile(numberSet, .75, method='weibull')
    iqr = q3 - q1
    return q3 + 1.5 * iqr

def stdev(numberSet, population_type="sample"):
    match population_type:
        case "sample":
            return statistics.stdev(numberSet)
        case "population" | "pop":
            return statistics.pstdev(numberSet)

def tan(n, unit='degrees'):
    deg = unit.lower().startswith('deg')
    if deg: n = deg2rad(n)
    return math.tan(n)
def sin(n, unit='degrees'):
    deg = unit.lower().startswith('deg')
    if deg: n = deg2rad(n)
    return math.sin(n)
def cos(n, unit='degrees'):
    deg = unit.lower().startswith('deg')
    if deg: n = deg2rad(n)
    return math.cos(n)
def cot(n, unit='degrees'):
    deg = unit.lower().startswith('deg')
    if deg: n = deg2rad(n)
    return 1 / math.tan(n)
def csc(n, unit='degrees'):
    deg = unit.lower().startswith('deg')
    if deg: n = deg2rad(n)
    return 1 / math.sin(n)
def sec(n, unit='degrees'):
    deg = unit.lower().startswith('deg')
    if deg: n = deg2rad(n)
    return 1 / math.cos(n)


clear = lambda: os.system("clear")
# clear = lambda: os.system("clear && printf '\e[3J'") # alternative. Clears saved lines if your terminal doesn't do this by default

if var_args.get('e') != None:
    ui = var_args.get('e')
    fixedString = fixUI(ui)
    if fixedString != None:
        try:
            result = eval(fixedString)
        except Exception as _e:
            exit(_e)
        if isNumber(result) and result < sys.float_info.max:
            print(f"{result:e}") if result >= 1e18 else print(f"{result:,}")
        else:
            print(result)
    exit()

while True:
    try:
        ui = uiSession.prompt(">")
        exitAttempts = 0
        match ui:
            case "" | None:
                continue
            case "clear":
                clear()
            case _:
                fixedString = fixUI(ui)
                if fixedString != None:
                    result = eval(fixedString)
                    if isNumber(result):
                        addToHistory(ui, result)
                        if result >= 1e18 and result < sys.float_info.max:
                            print(f"{result:e}")
                        else:
                            print(f"{result:,}")
                    elif isinstance(result, list):
                        addToHistory(ui, result)
                        print(result)
                    elif result != None:
                        print(result)
    except KeyboardInterrupt:
        if exitAttempts >= 1:
            print("\nTerminating script ...")
            exit()
        exitAttempts += 1
        print("\nConfirm exit via ctrl+C or ctrl+D")
    except EOFError:
        print("\nTerminating script ...")
        exit()
    except Exception as _e:
        print(_e)
        #print(sys.exc_info()[-1].tb_lineno, type(_e).__name__) get line of error

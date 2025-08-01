import sympy
import scipy
import scipy.special
import numpy
import statistics
import fractions
import math
from math import (
    sinh,
    cosh,
    tanh,
)
import re
import decimal
from datetime import datetime
from handlers._fixUi import *
from handlers._validators import *
from handlers._mathConstants import *

__all__ = [
    "mean",
    "average",
    "avg",
    "ptp",
    "inf", "infinity",
    "isprime",
    "showhelp",
    "prettyfraction",
    "fraction",
    "deg2rad",
    "rad2deg",
    "log",
    "root",
    "round5up",
    "round5down",
    "nCr",
    "nPr",
    "binomial",
    "integrate",
    "integral",
    "lim",
    "Lim",
    "trunc",
    "zscore",
    "z2pRange",
    "p2zRange",
    "uncertainty",
    "distance",
    "mass",
    "time",
    "volume",
    "quantile",
    "score2p",
    "outliers",
    "IQR",
    "lowerfence",
    "upperfence",
    "stdev",
    "clock",
    "storage",
    "sigfig",
    "roundsigfig",
    "sigfigs",
    "temperature",
    "exp2dec",
    "tan",
    "tanh",
    "arctan",
    "sin",
    "sinh",
    "arcsin",
    "cos",
    "cosh",
    "arccos",
    "cot",
    "csc",
    "sec",
    "howlongago",
    "lambertw",
    "W",
    "solve",
    "erfinv",
    "erfcinv",
]

def mean(multiset: list, no_outliers: bool = False):
    """Returns the average of a multiset of numbers.
    Usage:
        mean(multiset, no_outliers)
    Example:
        mean([1, 2, 3, 4, 1000], no_outliers=True) -> 2.5
    Parameters:
        multiset (array):    multiset of numbers used to calculate the mean
        no_outliers (bool):  removes outliers from multiset before calculating the average"""
    if no_outliers:
        _upper = upperfence(multiset)
        _lower = lowerfence(multiset)
        fixedMultiset = []
        for num in multiset:
            if num < _lower:
                continue
            elif num > _upper:
                continue
            fixedMultiset.append(num)
        return sum(fixedMultiset) / len(fixedMultiset)
    return sum(multiset) / len(multiset)
average, avg = mean, mean

def ptp(numberMultiSet):
    """Returns the range of a multiset of numbers. The function "ptp" stands for "peak to peak."
    Usage:
        ptp(numberMultiSet)
    Example:
        ptp([4, 5, 6]) -> 2
    Parameters:
        numberMultiSet (array): multiset of numbers used to calculate the range"""
    if isinstance(numberMultiSet, list) == False:
        raise TypeError("must be array")
    return max(numberMultiSet) - min(numberMultiSet)
inf, infinity = math.inf, math.inf
isprime = sympy.isprime

def showhelp(functionName=None):
    """Shows info about a function.
    Usage:
        showhelp(functionName)
    Examples:
        showhelp()
        showhelp(log)
    Parameters:
        functionName (function): name of function to display help"""
    if functionName == None:
        return showhelp.__doc__
    elif callable(functionName):
        return functionName.__doc__

def prettyfraction(numerator, denominator):
    """Returns a prettified visualization of a fraction.
    Usage:
        prettyFraction(numerator, denominator)
    Example:
        prettyFraction(1, 2)
    Parameters:
        numerator (int,float):   numerator of which will be visualized
        denominator (int,float): denominator of which will be visualized"""
    numeratorLength = len(str(numerator))
    denominatorLength = len(str(denominator))
    if numeratorLength == denominatorLength:
        seperatorLength = denominatorLength
        return StringedNumber(f"{numerator}\n{'-'*seperatorLength}\n{denominator}", addHistory=False)
    elif numeratorLength > denominatorLength:
        seperatorLength = numeratorLength
        steps = (seperatorLength - denominatorLength) // 2
        return StringedNumber(f"{numerator}\n{'-'*seperatorLength}\n{' '*steps}{denominator}", addHistory=False)
    elif numeratorLength < denominatorLength:
        seperatorLength = denominatorLength
        steps = (seperatorLength - numeratorLength) // 2
        return StringedNumber(f"{' '*steps}{numerator}\n{'-'*seperatorLength}\n{denominator}", addHistory=False)

def fraction(result: float, pretty=True) -> StringedNumber:
    """Returns a number as a fraction.
    Usage:
        fraction(result, pretty=True)
    Example:
        fraction(1/3) -> 1/3
    Parameters:
        result (float):           the number of which to be visualized as a fraction
        pretty, optional (bool):  displays the result in pretty mode"""
    global ans
    if not isinstance(result, float):
        return result
    ans = result
    resultInteger = int(result)
    resultDecimal = result - resultInteger
    if resultDecimal == 0:
        return result
    result_fraction = fractions.Fraction(resultDecimal).limit_denominator(1_000_000)
    if resultInteger == 0 and pretty:
        regexFractionSearch = re.search(r"(?P<num>\d+)/(?P<den>\d+)", str(result_fraction))
        result_pretty = prettyfraction(regexFractionSearch.group("num"), regexFractionSearch.group("den"))
        addToHistory(str(result), str(result_fraction), includeAll=True)
        return result_pretty
    if resultInteger > 0 and pretty:
        regexFractionSearch = re.search(r"(?P<num>\d+)/(?P<den>\d+)", str(result_fraction))
        result_pretty = prettyfraction(regexFractionSearch.group("num"), regexFractionSearch.group("den"))
        addToHistory(str(result), str(result_fraction), includeAll=True)
        return StringedNumber(f"{result_pretty.num} \x1b[1A+ {resultInteger}\n", addHistory=False)
    elif resultInteger > 0 and not pretty:
        addToHistory(str(result), str(result_fraction), includeAll=True)
        return StringedNumber(f"{resultInteger} + {result_fraction}", addHistory=False)
    addToHistory(str(result), str(result_fraction))
    return StringedNumber(str(result_fraction), addHistory=False)

# more functions
def deg2rad(deg):
    """Returns degrees to radians.
    Usage:
        deg2rad(deg)
    Example:
        deg2rad(180) -> 3.141...
    Parameters:
        deg (int): degrees"""
    return deg * (pi / 180)

def rad2deg(rad):
    """Returns radians to degrees.
    Usage:
        rad2deg(rad)
    Example:
        rad2deg(pi) -> 180
    Parameters:
        rad (int): radians"""
    return rad * (180 / pi)

def log(base, n):
    """Returns the log of a number.
    Usage:
        log(base, n)
    Example:
        log(2, 16) -> 4
    Parameters:
        base (int): the base of the logarithm
        n (int):    the number for which the logarithm needs to be calculated"""
    return math.log10(n) / math.log10(base)

def root(nth, n):
    """Returns the nth root.
    Usage:
        root(nth, n)
    Example:
        root(2, 9) -> 3
    Parameters:
        nth (int): the specified nth root
        n (int):   the number for which the nth root needs to be found"""
    result = pow(n, 1/nth)
    if result.is_integer():
        return int(result)
    return result

def round5up(num, prec=0):
    """Rounds 5 up.
    Usage:
        round5up(num, prec=0)
    Example:
        round5up(2.5, 0) -> 3
    Parameters:
        num (float): number to round
        prec (int):  number of decimal places to round"""
    num = num * 10**prec
    result = decimal.Decimal(num).quantize(0, decimal.ROUND_HALF_UP)
    result /= 10**prec
    if prec == 0:
        return int(result)
    return float(result)

def round5down(num, prec=0):
    """Rounds 5 down.
    Usage:
        round5down(num, prec=0)
    Example:
        round5down(2.5, 0) -> 2
    Parameters:
        num (float): number to round
        prec (int):  number of decimal places to round"""
    num = num * 10**prec
    result = decimal.Decimal(num).quantize(0, decimal.ROUND_HALF_DOWN)
    result /= 10**prec
    if prec == 0:
        return int(result)
    return (float(result))

def nCr(n, r):
    """Number of combinations.
    Usage:
        nCr(n, r)
    Example:
        nCr(5, 2) -> 10
    Parameters:
        n (int): total number of items
        r (int): number of items to be chosen"""
    return math.factorial(n) // ( math.factorial(r) * math.factorial(n - r) )

def nPr(n, r):
    """Number of permutations.
    Usage:
        nPr(n, r)
    Example:
        nPr(5, 2) -> 20
    Parameters:
        n (int): total number of items
        r (int): number of items to be chosen"""
    return math.factorial(n) // math.factorial(n - r)

def binomial(p, n, x):
    """Finds binomial probability.
    Usage:
        binomial(p, n, x)
    Example:
        binomial(0.5, 3, 1) -> 0.375
    Parameters:
        p (float): probability of success
        n (int):   number of trials
        x (int):   number of successes"""
    numberOfCombinations = nCr(n, x)
    q = 1 - p
    binomialProbability = numberOfCombinations * p**x * q**(n - x)
    return binomialProbability

def integrate(f, lower=None, upper=None, pretty=True):
    """Uses sympy's `integrate` function to compute definite or indefinite integrals.
    Usage:
        integrate(f, lower=None, upper=None, pretty=True)
    Examples:
        integrate("2 * x", 1, 10) -> 99
        integrate("2 * x") -> x**2
    Parameters:
        f (str):                  expression to integrate
        lower, optional (int):    lower end of integral
        upper, optional (int):    upper end of integral
        pretty, optional (bool):  pretty print mode
    """
    if lower != None and upper != None:
        result = sympy.integrate(f, ('x', lower, upper))
        newExpression = f"integrate({f}, lower={lower}, upper={upper})"
        addToHistory(newExpression, str(result), includeAll=True)
        if pretty:
            return sympy.pprint(result)
        else:
            return result
    if lower == None and upper == None:
        result = sympy.integrate(f)
        newExpression = f"integrate({f})"
        addToHistory(newExpression, str(result), includeAll=True)
        if pretty:
            return sympy.pprint(result)
        else:
            return result
    raise ValueError("both upper and lower must have values")
def integral(f, pretty=True):
    """Uses sympy's `Integral` function to represent unevaluated integrals.
    Usage:
        integral(f, pretty=True)
    Example:
        integral("2 * x") -> Integral(2*x, x)
    Parameters:
        f (str):                 expression to represent
        pretty, optional (bool): pretty print mode"""
    result = sympy.Integral(f)
    newExpression = f"integral({f})"
    addToHistory(newExpression, str(result), includeAll=True)
    if pretty:
        return sympy.pprint(result)
    elif not pretty:
        return result
    return "Error"

def lim(f, x):
    """Uses sympy's `limit` function to compute the limit of `f` at the point `x`.
    Usage:
        lim(f, x)
    Example:
        lim("x**2 + 2*x - 4", 5) -> 31
    Parameters:
        f (str):           expression representing the variable in the limit
        x (int,float,str): the value toward which `x` tends"""
    result = float( sympy.limit(f, 'x', x) )
    return result

def Lim(f, x, pretty=True):
    """Uses sympy's `Limit` function to represent an unevaluated limit.
    Usage:
        Lim(f, x, pretty=True)
    Example:
        Lim("x**2 + 2*x - 4", 5)
    Parameters:
        f (str):                 expression to represent
        x (int,float,str):       value for `x`
        pretty, optional (bool): pretty print mode"""
    if pretty:
        result = sympy.pprint(sympy.Limit(f, 'x', x))
    else:
        result = sympy.Limit(f, 'x', x)
    return result

def trunc(num, prec=0):
    """Truncates a number.
    Usage:
        trunc(num, prec=0)
    Example:
        trunc(1.2498, 2) -> 1.24
    Parameters:
        num (float): number of which to truncate
        prec (int):  number of decimal places to keep"""
    if isinstance(num, float) == False:
        raise TypeError("number must be float")
    decimals = re.sub(r"^(?:-?\d+\.|\.|-\.)(?P<decimals>\d+)$", r"\g<decimals>", str(num))
    if prec > len(decimals):
        return num
    if prec < 0:
        raise ValueError("precision is below zero")
    elif prec == 0:
        return int(num)
    if num == 0:
        return 0
    elif num > 0:
        return math.floor(num * 10**prec) / 10**prec
    elif num < 0:
        return math.ceil(num * 10**prec) / 10**prec
    return None

def zscore(score, mean, sd):
    """Returns the z-score of a value given the mean and standard deviation.
    Usage:
        zscore(score, mean, sd)
    Example:
        zscore(160, 100, 15) -> 4
    Parameters:
        score (int,float): value of which to calculate the z-score
        mean (int,float):  mean value of data
        sd (int,float):    standard deviation of data"""
    return ((score - mean) / sd)

def z2pRange(z1, z2):
    """Returns the normal distribution cumulative distribution function between two values. Uses scipy's `stats.norm.cdf` function.
    Usage:
        z2pRange(z1, z2)
    Example:
        z2pRange(-1, 1) -> 0.68...
    Parameters:
        z1 (int,float): lower end of value
        z2 (int,float): upper end of value"""
    p = scipy.stats.norm.cdf(z2) - scipy.stats.norm.cdf(z1)
    return p

def p2zRange(p1, p2):
    """Returns the normal distribution percent point function between two values. Uses scipy's `stats.norm.ppf` function.
    Usage:
        p2zRange(p1, p2)
    Example:
        p2zRange(0.5, 0.84) -> 0.994...
    Parameters:
        p1 (int,float): lower end probability
        p2 (int,float): upper end probability"""
    z = scipy.stats.norm.ppf(p2) - scipy.stats.norm.ppf(p1)
    return z

def uncertainty(numberMultiset):
    """Returns the uncertainty of a multiset of numbers.
    Usage:
        uncertainty(numberMultiSet)
    Example:
        uncertainty([1, 2, 3]) -> 1
    Parameters:
        numberMultiSet (array): number multiset of which to calculate the uncertainty
    Note:
        Uncertainty results are commonly rounded to 1 significant figure."""
    numberMultiSetRange = max(numberMultiset) - min(numberMultiset)
    result = numberMultiSetRange / 2
    if result.is_integer():
        return int(result)
    return result

def distance(n, unit1, unit2):
    """Returns the distance of a value converted into another unit.
    Usage:
        distance(n, unit1, unit2)
    Example:
        distance(1, "m", "ft") -> 3.28...
    Parameters:
        n (int,float): initial value
        unit1 (str):   distance unit being used
        unit2 (str):   unit to convert to
    Units:
        pm -> picometers
        nm -> nanometers
        um -> micrometers
        mm -> millimeters
        cm -> centimeters
        dm -> decimeters
        km -> kilometers
        ly -> light years
        in -> inches
        ft -> feet
        yd -> yards
        mi -> miles
        au -> astronomical unit
        pc -> parsec
        planck -> planck length"""
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
    """Returns the mass of a value converted into another unit.
    Usage:
        mass(n, unit1, unit2)
    Example:
        mass(1, "kg", "lb") -> 2.2...
    Parameters:
        n (int,float):  initial value
        unit1 (str):    mass unit being used
        unit2 (str):    unit to convert to
    Units:
        kg -> kilograms
        pg -> picogram
        ng -> nanograms
        ug -> micrograms
        mg -> milligrams
        g -> grams
        t -> metric ton
        gr -> grain
        oz -> ounce
        lb -> pound
        st -> stone
        ton -> US ton
        planck -> planck mass"""
    units = {
        "kg": 1,
        "pg": 1e-15,
        "ng": 1/1e12,
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
    """Returns time converted into another unit.
    Usage:
        time(n, unit1, unit2)
    Example:
        time(1, 'min', 's') -> 60
    Parameters:
        n (int,float):  initial value
        unit1 (str):    time unit being used
        unit2 (str):    unit to convert to
    Units:
        ns -> nanosecond
        us -> microsecond
        ms -> millisecond
        min -> minute
        h -> hour
        d -> days
        wk -> weeks
        a -> julian year
        planck -> planck time"""
    units = {
        "s": 1,
        "ns": 1e-9,
        "us": 1/1e6,
        "ms": 1/1e3,
        "min": 60,
        "h": 3600,
        "d": 86400,
        "wk": 86400*7,
        "a": 365.25*86400,
        "planck": 5.391247E-44,
    }
    multiplier = units.get(unit1) # multiply by this to get seconds
    n_s = n * multiplier
    return n_s / units.get(unit2)

def volume(n, unit1, unit2):
    """Returns a volume value converted into another unit.
    Usage:
        volume(n, unit1, unit2)
    Example:
        volume(1, 'bbl', 'gal') -> 42
    Parameters:
        n (int,float):  initial value
        unit1 (str):    volume unit being used
        unit2 (str):    unit to convert to
    Units:
        l -> liter
        gtt -> drop
        ml -> milliliters
        tsp -> metric teaspoon
        tbsp -> metric tablespoon
        imp_floz -> imperial fluid ounce
        imp_qt -> imperial quart
        floz -> US fluid ounce
        dl -> deciliter
        c -> US cup
        pt -> US pint
        imp_pt -> imperial pint
        qt -> US quart
        gal -> US gallon
        imp_gal -> imperial gallon
        bbl -> oil barrel"""
    units = {
        "l": 1,
        "gtt": 0.00005,
        "ml": 0.001,
        "tsp": 0.005,
        "tbsp": 0.015,
        "imp_floz": 0.0284130625,
        "floz": 0.0295735295625,
        "dl": 0.1,
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

def quantile(numberMultiSet, p, method='weibull'):
    """Returns the value of a given percentile.
    Usage:
        quantile(numberMultiSet, p, method='weibull')
    Example:
        quantile([1, 8, 4, 9], 0.5) -> 6
    Parameters:
        numberMultiSet (array):       multiset of numbers used to calculate the value
        p (float):                    percentile as a decimal (0 to 1)
        method, optional (str):       method used with numpy's `quantile` function. See `numpy.quantile` for more info."""
    result = numpy.quantile(numberMultiSet, p, method=method)
    return result

def score2p(numberMultiSet, score, method='weak'):
    """Returns the percentile of a given value as a decimal.
    Usage:
        score2p(numberMultiSet, score, method='weak')
    Example:
        score2p([1, 8, 4, 9], 6) -> 0.5
    Parameters:
        numberMultiSet (array): multiset of numbers used to calculate the percentile decimal
        score (int,float):      score of which to calculate the percentile
        method, optional (str): method used with scipy's `percentileofscore` function. See `scipy.stats.percentileofscore` for more info."""
    return scipy.stats.percentileofscore(numberMultiSet, score, kind=method) / 100

def outliers(numberMultiSet):
    """Returns a list of outliers in a multiset of numbers based on the 1.5 IQR rule.
    Usage:
        outliers(numberMultiSet)
    Example:
        outliers([1, 9, 4, 200, 5, 10]) -> [200]
    Parameters:
        numberMultiSet (array): multiset of numbers used to calculate the outliers"""
    outlierMultiSet = []
    q1 = quantile(numberMultiSet, .25, method='weibull')
    q3 = quantile(numberMultiSet, .75, method='weibull')
    iqr = q3 - q1
    lowerFence = q1 - 1.5 * iqr
    higherFence = q3 + 1.5 * iqr
    for num in numberMultiSet:
        if num < lowerFence or num > higherFence:
            outlierMultiSet.append(num)
    return outlierMultiSet

def IQR(numberMultiSet):
    """Returns the interquartile range (IQR).
    Usage:
        IQR(numberMultiSet)
    Example:
        IQR([1, 100, 90, 50]) -> 84.25
    Parameters:
        numberMultiSet (array): multiset of numbers used to calculate the IQR"""
    q1 = quantile(numberMultiSet, .25, method='weibull')
    q3 = quantile(numberMultiSet, .75, method='weibull')
    iqr = q3 - q1
    return iqr

def lowerfence(numberMultiSet):
    """Returns the lower fence of a multiset of numbers.
    Usage:
        lowerfence(numberMultiSet)
    Example:
        lowerfence([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]) -> -7
    Parameters:
        numberMultiSet (array): multiset of numbers used to calculate the lowerfence"""
    q1 = quantile(numberMultiSet, .25, method='weibull')
    q3 = quantile(numberMultiSet, .75, method='weibull')
    iqr = q3 - q1
    return q1 - 1.5 * iqr

def upperfence(numberMultiSet):
    """Returns the upper fence of a multiset of numbers.
    Usage:
        upperfence(numberMultiSet)
    Example:
        upperfence([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]) -> 17
    Parameters:
        numberMultiSet (array): multiset of numbers used to calculate the upperfence"""
    q1 = quantile(numberMultiSet, .25, method='weibull')
    q3 = quantile(numberMultiSet, .75, method='weibull')
    iqr = q3 - q1
    return q3 + 1.5 * iqr

def stdev(numberMultiSet, population_type="sample"):
    """Returns the standard deviation of a multiset of numbers.
    Usage:
        stdev(numberMultiSet, population_type='sample')
    Examples:
        stdev([1, 2, 3]) -> 1
        stdev([1, 2, 3], population_type='population') -> 0.816...
    Parameters:
        numberMultiSet (array):          multiset of numbers used to calculate the standard deviation
        population_type, optional (str): type of population
    Population Types:
        sample
        population or pop"""
    if isinstance(numberMultiSet, list) == False:
        raise TypeError("number multiset must be an array")
    match population_type:
        case "sample":
            return statistics.stdev(numberMultiSet)
        case "population" | "pop":
            return statistics.pstdev(numberMultiSet)

def clock(clockTime, unit='s'):
    """Returns time or time into day.
    Usage:
        clock(clockTime, unit='s')
    Examples:
        clock("20:30:00") -> 73,800 # seconds into the day
        clock("21:30:00", 'h') -> 9.5 # hours into the day
        clock("1800", 'min') -> 1,080 # minutes into the day
        clock(86395) -> "23:59:55"
    Parameters:
        clockTime (str,int,float): time in 24-hour format or time into the day
        unit, optional (str):      unit of time
    Units:
        us -> microsecond
        ms -> millisecond
        min -> minute
        h -> hour
        d -> days
        wk -> weeks
        a -> julian year
        planck -> planck time"""
    if isinstance(clockTime, str):
        clockCivSearch = re.search(r"^(\d{1,2}):(\d{2})(?::(\d{2}))?$", clockTime)
        clockMilSearch = re.search(r"^(\d{2})(\d{2})(?::(\d{2}))?$", clockTime)
        isCiv = clockCivSearch != None
        isMil = clockMilSearch != None
        if isCiv:
            clockHands = (clockCivSearch.group(1), clockCivSearch.group(2), clockCivSearch.group(3) if clockCivSearch.group(3) != None else 0)
        elif isMil:
            clockHands = (clockMilSearch.group(1), clockMilSearch.group(2), clockMilSearch.group(3) if clockMilSearch.group(3) != None else 0)
        else:
            raise ValueError("invalid clock time format")
        clockHands = tuple([int(clockHands[i]) for i in range(len(clockHands))])
        if not clockHands[1] in range(0, 60) or not clockHands[2] in range(0, 60):
            raise ValueError("minutes or seconds must be no less than 0 and not greater than 60")
        timeElapsed = clockHands[0] * 3600 + clockHands[1] * 60 + clockHands[2]
        return time(timeElapsed, "s", unit)
    if unit != "s":
        clockTime = time(clockTime, unit, "s")
    clockHour = int(clockTime // 3600)
    clockMinute = int((clockTime - clockHour*3600) // 60)
    clockSeconds = round5up(clockTime - clockHour * 3600 - clockMinute * 60, 3)
    clockHour, clockMinute = str(clockHour).zfill(2), str(clockMinute).zfill(2)
    if clockSeconds.is_integer():
        clockSeconds = str(int(clockSeconds)).zfill(2)
    else:
        clockSeconds = f"{str(int(clockSeconds)).zfill(2)}.{str(clockSeconds)[str(clockSeconds).find('.')+1:]}"
    return StringedNumber("%s:%s:%s" % (clockHour, clockMinute, clockSeconds))

def howlongago(clockTime, unit='s'):
    """Returns how much time has passed since the specified clock time.
    Usage:
        howlongago(clockTime, unit='s')
    Examples:
        howlongago("0100", 'h') -> 1
        howlongago("01:00", 'min') -> 60
    Parameters:
        clockTime (str):      time in 24-hour format
        unit, optional (str): unit of time
    Units:
        us -> microsecond
        ms -> millisecond
        min -> minute
        h -> hour
        d -> days
        wk -> weeks
        a -> julian year
        planck -> planck time"""
    clockCivSearch = re.search(r"^(\d{1,2}):(\d{2})(?::(\d{2}))?$", clockTime)
    clockMilSearch = re.search(r"^(\d{2})(\d{2})(?::(\d{2}))?$", clockTime)
    isMil = clockMilSearch != None
    hasSecondsHand = clockMilSearch.group(3) != None if isMil else clockCivSearch.group(3) != None
    clockSecondsHand = (clockMilSearch.group(3) if isMil else clockCivSearch.group(3)) if hasSecondsHand else 0
    clockHands = (
        int(clockMilSearch.group(1) if isMil else clockCivSearch.group(1)),
        int(clockMilSearch.group(2) if isMil else clockCivSearch.group(2)),
        int(clockSecondsHand),
    )
    currentDate = datetime.now().date()
    howLongAgoResult = datetime(currentDate.year, currentDate.month, currentDate.day, clockHands[0], clockHands[1], clockHands[2])
    howLongAgoResult = datetime.now().timestamp() - howLongAgoResult.timestamp()
    return howLongAgoResult if unit == "s" else time(howLongAgoResult, "s", unit)

def storage(n, unit1, unit2):
    """Returns data sizes converted into another unit.
    Usage:
        storage(n, unit1, unit2)
    Information:
        Using lowercase "b" will use bits instead of bytes.
    Examples:
        storage(1000, 'B', 'kB') -> 1
        storage(1, 'B', 'b') -> 8
    Parameters:
        n (int,float): initial value
        unit1 (str):   unit to convert from
        unit2 (str):   unit to convert to
    Units:
        B -> byte
        kB -> kilobyte
        MB -> megabyte
        GB -> gigabyte
        TB -> terabyte
        PB -> petabyte
        EB -> exabyte
        ZB -> zettabyte
        YB -> yottabyte
        RB -> ronnabyte
        QB -> quettabyte
        KiB -> kibibyte
        MiB -> mebibyte
        GiB -> gibibyte
        TiB -> tebibyte
        PiB -> pebibyte
        EiB -> exbibyte
        ZiB -> zebibyte
        YiB -> yobibyte"""
    units = {
        "B": 1,
        "kB": 1E3,
        "MB": 1E3**2,
        "GB": 1E3**3,
        "TB": 1E3**4,
        "PB": 1E3**5,
        "EB": 1E3**6,
        "ZB": 1E3**7,
        "YB": 1E3**8,
        "RB": 1E3**9,
        "QB": 1E3**10,
        "KiB": 1024,
        "MiB": 1024**2,
        "GiB": 1024**3,
        "TiB": 1024**4,
        "PiB": 1024**5,
        "EiB": 1024**6,
        "ZiB": 1024**7,
        "YiB": 1024**8,
    }
    useBits = unit1.endswith('b')
    returnBits = unit2.endswith('b')
    if useBits:
        unit1 = unit1.replace('b', 'B')
    if returnBits:
        unit2 = unit2.replace('b', 'B')
    multiplier = units.get(unit1) # multiply by this to get bytes
    if useBits:
        multiplier *= (1/8)
    n_bytes = n * multiplier
    if returnBits:
        return n_bytes / (units.get(unit2) * (1/8))
    return n_bytes / units.get(unit2)


def sigfig(num):
    """Returns how many significant figures are in a number.
    Usage:
        sigfig(num)
    Examples:
        sigfig(100) -> 1
        sigfig("100.00") -> 5
        sigfig([100, 101, "100.0"]) -> {100: 1, 101: 3, '100.0': 4}
    Parameters:
        num (int,str,array): number(s) for which to count the number of sigfigs"""
    if isinstance(num, (int, str, list)) == False:
        raise TypeError("numbers must integers or strings")
    isArray = isinstance(num, list)
    if isArray:
        sigFigList = {}
        for n in num:
            numString = str(n)
            numIsInt = numString.isnumeric()
            if numIsInt:
                numString = re.sub(r"[\-\.]", '', numString)
                numString = numString.lstrip('0')
                numString = numString.rstrip('0')
                sigFigs = len(numString)
                sigFigList[n] = sigFigs
            elif isNumber(n):
                numString = re.sub(r"[\-\.]", '', numString)
                numString = numString.lstrip('0')
                sigFigs = len(numString)
                sigFigList[n] = sigFigs
        return sigFigList
    numString = str(num)
    numIsInt = numString.isnumeric()
    if numIsInt:
        if numString.endswith('.'):
            sigFigs = len(numString.lstrip('0').replace('.', ''))
            return sigFigs
        numString = re.sub(r"[\-\.]", '', numString)
        numString = numString.lstrip('0')
        numString = numString.rstrip('0')
        sigFigs = len(numString)
        return sigFigs
    elif isNumber(num):
        numString = re.sub(r"[\-\.]", '', numString)
        numString = numString.lstrip('0')
        sigFigs = len(numString)
        return sigFigs

def roundsigfig(num, prec=1):
    """Returns a number rounded by a certain amount of sigfigs.
    Usage:
        roundsigfig(num, prec=1)
    Examples:
        roundsigfig(1500, 1) -> 2000
        roundsigfig("0.00259", 2) -> 0.0026
    Parameters:
        num (int,str): number of which to round sigfigs
        prec (int):    number of sigfigs to round to
    Note:
        Rounding very large numbers can possibly lead to slight inaccuracies, for example, a number may end with '999...', this is because of how python handles floats.
        It is recommended to learn how to round sigfigs without relying on calculators."""
    if isinstance(num, (int, str)) == False:
        raise TypeError("number must be integer or string")
    if prec <= 0:
        raise ValueError("precision is less than or equal to zero")
    isNegative = float(num) < 0
    num = abs(float(num))
    numString = str(num)
    initialSigFigs = sigfig(numString)
    if initialSigFigs < prec:
        raise ValueError("precision too high")
    if prec == initialSigFigs:
        if isNegative:
            num = f"-{num}"
        if isinstance(num, int):
            return StringedNumber(num, returnAsInt=True)
        return StringedNumber(num)
    isInt = numString.isnumeric()
    if isInt:
        numAsDecimal = int(numString) / 10**len(numString)
        roundedValue = round5up(numAsDecimal, prec)
        roundedValue *= 10**len(numString)
        roundedValue = int(roundedValue)
        resultSigFigs = sigfig(str(roundedValue))
        if resultSigFigs != prec:
            currentResult = str(int(roundedValue))[:prec] + "\u0305" + str(int(roundedValue))[prec:]
            return StringedNumber(currentResult)
        return StringedNumber(roundedValue, returnAsInt=True)
    elif isNumber(numString):
        numString = exp2dec(float(numString)) # precision update
        digitPos = numString.index('.')
        numStringNoJunk = re.sub(r"[\-\.]", '', numString)
        numStringFirstSigFigPos = re.search("[1-9]", numStringNoJunk).start()
        numStringNoLeadingZeros = numStringNoJunk[numStringFirstSigFigPos:]
        numAsDecimal = int(numStringNoLeadingZeros) / 10**len(numStringNoLeadingZeros)
        roundedValue = round5up(numAsDecimal, prec)
        roundedValue /= 10**(numStringFirstSigFigPos-digitPos)
        roundedValue = exp2dec(roundedValue)
        digitsWithoutDecimal = len(str(int(float(roundedValue))))
        if float(roundedValue) >= 1:
            roundedValue = decimal.Decimal(roundedValue).quantize(decimal.Decimal('0.' + '0' * (prec-digitsWithoutDecimal)), context=decimal.Context(prec=len(numString), rounding=decimal.ROUND_HALF_UP))
            resultSigFigs = sigfig(str(roundedValue))
            if resultSigFigs != prec:
                currentResult = str(roundedValue)[:prec] + "\u0305" + str(roundedValue)[prec:]
                return StringedNumber(currentResult)
            if isNegative:
                roundedValue = f"-{roundedValue}"
            return StringedNumber(roundedValue)
        resultSigFigs = sigfig(roundedValue)
        if resultSigFigs > initialSigFigs:
            firstSigFigPos = re.search("[1-9]", roundedValue).start()
            endPos = firstSigFigPos + prec
            roundedValue = roundedValue[:endPos]
            return StringedNumber(roundedValue)
        if resultSigFigs < initialSigFigs:
            missingSigFigs = prec - resultSigFigs
            roundedValue = str(roundedValue) + '0'*(missingSigFigs)
            return StringedNumber(roundedValue)
        return StringedNumber(roundedValue)

def sigfigs(num):
    """Returns the significant figures of a number.
    Usage:
        sigfigs(num)
    Examples:
        sigfigs(100) -> ['1']
        sigfigs("100.0") -> ['1', '0', '0', '0']
    Parameters:
        num (int,str): number for which sigfigs will be displayed"""
    if isinstance(num, (int, str)) == False:
        raise TypeError("number must be integer or string")
    numString = str(num)
    isInt = numString.isnumeric()
    sigFigArray = []
    if isInt:
        sigFigs = numString.rstrip('0')
        for c in sigFigs:
            sigFigArray.append(c)
        return sigFigArray
    elif isNumber(numString):
        numStringNoJunk = re.sub(r"[\-\.]", '', numString)
        firstSigFigPos = re.search("[1-9]", numStringNoJunk).start()
        sigFigs = numStringNoJunk[firstSigFigPos:]
        if sigFigs != '':
            for c in sigFigs:
                sigFigArray.append(c)
        return sigFigArray

def temperature(num, unit1, unit2):
    """Returns temperature values converted into another unit.
    Usage:
        temperature(num, unit1, unit2)
    Examples:
        temperature(32, 'f', 'c') -> 0
        temperature(2.7, 'k', 'c') -> -270.45
    Parameters:
        num (int,float): initial temperature
        unit1 (str):     unit to convert from
        unit2 (str):     unit to convert to
    Units:
        c -> celcius
        f -> fahrenheit
        k -> kelvin
        planck -> planck temperature"""
    if unit1 == unit2:
        return num
    conversionType = f"{unit1}2{unit2}"
    planckTemp = 1.416784e+32
    match conversionType:
        case "c2f":
            return num * (9/5) + 32
        case "c2k":
            return num + 273.15
        case "f2c":
            return (num - 32) * (5/9)
        case "f2k":
            return (num - 32) * (5/9) + 273.15
        case "k2c":
            return num - 273.15
        case "k2f":
            return (num - 273.15) * (9/5) + 32
        case "planck2c":
            return (num * planckTemp) - 273.15
        case "planck2f":
            return ((num * planckTemp) - 273.15) * (9/5) + 32
        case "planck2k":
            return num * planckTemp
        case "c2planck":
            return (num + 273.15) / planckTemp
        case "f2planck":
            return ((num - 32) * (5/9) + 273.15) / planckTemp
        case "k2planck":
            return num / planckTemp
        case _:
            raise TypeError("invalid units")

def exp2dec(num):
    if isinstance(num, (float)) == False:
        raise TypeError("number must be float")
    if num >= 1e16 or abs(num) < 1e-4:
        numStr = str(num)
        posAtE = numStr.index('e')
        hasDec = posAtE > 1
        numExponent = abs(floor(log10(abs(num))))
        if hasDec:
            newDec = posAtE - 2 + numExponent
            decForm = str("{:." + str(newDec) + "f}").format(num)
            return str(decForm)
        else:
            decForm = str("{:." + str(numExponent) + "f}").format(num)
            return str(decForm)
    return str(num)

def tan(num, unit='rad'):
    """Returns tan of a number.
    Usage:
        tan(num, unit='rad')
    Examples:
        tan(45) -> 1.619...
        tan(45, 'deg') -> 1
    Parameters:
        num (int,float):      number to use
        unit, optional (str): unit to use
    Units:
        rad -> radians
        deg -> degrees"""
    if unit == "deg": num = math.radians(num)
    return math.tan(num)
def arctan(num, unit='rad'):
    """Returns arc tan of a number.
    Usage:
        arctan(num, unit='rad')
    Examples:
        arctan(pi) -> 1.262...
        arctan(45, 'deg') -> 1
    Parameters:
        num (int, float):     number to use
        unit, optional (str): unit to use
    Units:
        rad -> radians
        deg -> degrees"""
    useDegrees = unit == "deg"
    result = math.degrees(math.atan(num)) if useDegrees else math.atan(num)
    return result
def sin(num, unit='rad'):
    """Returns sin of a number.
    Usage:
        sin(num, unit='rad')
    Examples:
        sin(90) -> 0.893...
        sin(90, 'deg') -> 1
    Parameters:
        num (int,float):      number to use
        unit, optional (str): unit to use
    Units:
        deg -> degrees
        rad -> radians"""
    if unit == "deg": num = math.radians(num)
    return math.sin(num)
def arcsin(num, unit='rad'):
    """Returns arc sin of a number.
    Usage:
        arcsin(num, unit='rad')
    Examples:
        arcsin(0.5, 'deg') -> 30
        arcsin(0.5) -> 0.523...
    Parameters:
        num (int, float):     number to use
        unit, optional (str): unit to use
    Units:
        deg -> degrees
        rad -> radians"""
    useDegrees = unit == "deg"
    result = math.degrees(math.asin(num)) if useDegrees else math.asin(num)
    return result
def cos(num, unit='rad'):
    """Returns cos of a number.
    Usage:
        cos(num, unit='rad')
    Examples:
        cos(360) -> -0.283...
        cos(360, 'deg') -> 1
    Parameters:
        num (int,float):      number to use
        unit, optional (str): unit to use
    Units:
        rad -> radians
        deg -> degrees"""
    if unit == "deg": num = math.radians(num)
    return math.cos(num)
def arccos(num, unit='rad'):
    """Returns arc cos of a number.
    Usage:
        arccos(num, unit='rad')
    Examples:
        arccos(0) -> 1.57...
        arccos(0, 'deg') -> 90
    Parameters:
        num (int, float):     number to use
        unit, optional (str): unit to use
    Units:
        rad -> radians
        deg -> degrees"""
    useDegrees = unit == "deg"
    result = math.degrees(math.acos(num)) if useDegrees else math.acos(num)
    return result
def cot(num, unit='rad'):
    """Returns cot of a number.
    Usage:
        cot(num, unit='rad')
    Examples:
        cot(1) -> 0.642...
        cot(1, 'deg') -> 57.289...
    Parameters:
        num (int,float):      number to use
        unit, optional (str): unit to use
    Units:
        rad -> radians
        deg -> degrees"""
    if unit == "deg": num = math.radians(num)
    return 1 / math.tan(num)
def csc(num, unit='rad'):
    """Returns csc of a number.
    Usage:
        csc(num, unit='rad')
    Examples:
        csc(1.57) -> 1.000...
        csc(1.57, 'deg') -> 36.498...
    Parameters:
        num (int,float):      number to use
        unit, optional (str): unit to use
    Units:
        rad -> radians
        deg -> degrees"""
    if unit == "deg": num = math.radians(num)
    return 1 / math.sin(num)
def sec(num, unit='rad'):
    """Returns sec of a number.
    Usage:
        sec(num, unit='rad')
    Examples:
        sec(pi*2) -> 1
        sec(pi*2, 'deg') -> 1.006...
    Parameters:
        num (int,float):      number to use
        unit, optional (str): unit to use
    Units:
        rad -> radians
        deg -> degrees"""
    if unit == "deg": num = math.radians(num)
    return 1 / math.cos(num)

def lambertw(*args, **kwargs):
    """Uses scipy's `lambertw` function.
    Usage:
        lambertw(*args, **kwargs)
    Examples:
        lambertw(2) -> 0.85"""
    return complex(scipy.special.lambertw(*args, **kwargs))
W = lambertw # alias for lambert W

def solve(equation: str, result: float):
    """Uses sympy to solve $x$.
    Usage:
        solve(equation, result)
    Examples:
        solve("x**2", 9) -> [-3, 3]
    Parameters:
        equation (str): equation used to solve for $x$
        result (float): the result of which will be used to solve for $x$"""
    equation = sympy.sympify(equation)
    equation = sympy.Eq(equation, result)
    solution = sympy.solve(equation, 'x')
    return solution

def erfinv(num: float):
    """Uses scipy's `erfinv` function.
    Usage:
        erfinv(num)
    Examples:
        erfinv(0.5) -> ~0.48"""
    return scipy.special.erfinv(num)

def erfcinv(num: float):
    """Uses scipy's `erfcinv` function.
    Usage:
        erfcinv(num)
    Examples:
        erfcinv(0.02212) -> ~1.618"""
    return scipy.special.erfcinv(num)

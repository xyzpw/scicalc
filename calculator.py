#!/usr/bin/env python3

import readline
import math
import os
import re
import statistics
import scipy
import warnings
import argparse

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
    "phi": f"Golden ratio {phi}"
}

# functions
log10 = math.log10
ln = math.log
log2 = math.log2
cbrt = math.cbrt
sqrt = math.sqrt
exp = math.exp
floor = math.floor
ceil = math.ceil
mean = statistics.mean; average = statistics.mean; avg = statistics.mean
mode = statistics.mode
median = statistics.median
#stdev = statistics.stdev
z2p = scipy.stats.norm.cdf
p2z = scipy.stats.norm.ppf
fact = math.factorial; factorial = math.factorial
normaltest = scipy.stats.normaltest

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
        "/": Symbols.divide
    }
    for sym, val in replacements.items():
        equation = re.sub(sym, val, equation)
    return equation

def addToHistory(equation, result):
    global history
    if isNumber(result):
        # remove last equation from history if the max. limit is reached
        if len(history) >= 40:
            history.pop(0)
        if result >= 1e18:
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

def nCr(n, r): return math.factorial(n) / ( math.factorial(r) * math.factorial(n - r) )

def nPr(n, r): return math.factorial(n) / math.factorial(n - r)

def trunc(n, p=0):
    if n == 0:
        return 0
    elif n > 0:
        return math.floor(n * 10**p) / 10**p
    elif n < 0:
        return math.ceil(n * 10**p) / 10**p
    return None

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
        "planck": 1.616255e-35
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
        "planck": 2.176434e-8
    }
    multiplier = units.get(unit1) # multiply by this to get kilograms
    n_kg = n * multiplier
    return n_kg / units.get(unit2)

def quantile(numberSet, p, method='weibull'):
    return scipy.quantile(numberSet, p, method=method)

def score2p(numberSet, score, method='weak'):
    return scipy.stats.percentileofscore(numberSet, score, kind=method) / 100

def outliers(numberSet):
    outlierSet = []
    Q1 = scipy.quantile(numberSet, .25, method='weibull')
    Q3 = scipy.quantile(numberSet, .75, method='weibull')
    IQR = Q3 - Q1
    lowerFence = Q1 - 1.5 * IQR
    higherFence = Q3 + 1.5 * IQR
    for num in numberSet:
        if num < lowerFence or num > higherFence:
            outlierSet.append(num)
    return outlierSet

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



def clear():
    os.system("clear")

if var_args.get('e') != None:
    ui = var_args.get('e')
    fixedString = fixUI(ui)
    if fixedString != None:
        result = eval(fixedString)
        if isNumber(result):
            exit(f"{result:e}") if result >= 1e16 else exit(f"{result:,}")
        else:
            exit(result)
    exit()

while True:
    try:
        ui = input(">")
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
                        if result >= 1e16:
                            print(f"{result:e}")
                        else:
                            print(f"{result:,}")
                    elif isinstance(result, list):
                        addToHistory(ui, result)
                        print(result)
                    else:
                        print(result)
    except KeyboardInterrupt:
        if exitAttempts >= 1: exit("\nTerminating script ...")
        exitAttempts += 1
        print("\nConfirm exit via ctrl+C or ctrl+D")
    except EOFError:
        exit("\nTerminating script ...")
    except Exception as _e:
        print(_e)

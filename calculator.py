#!/usr/bin/env python3

import readline
import math
import os
import re
import statistics
import scipy

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
    class Radicals:
        sqrt = '\u221a'
        cbrt = '\u221b'
    class Fractions:
        fourth = '\u00bc'
        half = '\u00bd'
        quarter3 = '\u00be'
        third = '\u2153'

# constants
c = 299792458
g = 9.8
G = 6.67430 * 10**-11
pi = math.pi
e = math.e
ly = 299792458 * (3600 * 24 * 365)
h = 6.62607015e-34
k = 1.380649e-23
phi = (1 + math.sqrt(5)) / 2

constants = {"c": f"Speed of light {c:,} m/s",
    "g": f"Standard gravity {g} m/s{Symbols.squared}",
    "G": f"Gravitational constant {G} N{Symbols.cdot}m{Symbols.squared}/kg{Symbols.squared}",
    "h": f"Planck's constant {h} J/Hz",
    "k": f"Boltzmann constant {k} J/K",
    "ly": f"1 light year {ly:,} m",
    "phi": f"Golden ratio {phi}"
}

# functions
log10 = math.log10
ln = math.log
log2 = math.log2
cbrt = math.cbrt
sqrt = math.sqrt
exp = math.exp
mean = statistics.mean
stdev = statistics.stdev
z2p = scipy.stats.norm.cdf
p2z = scipy.stats.norm.ppf
fact = math.factorial; factorial = math.factorial

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
    replacements = {"\*": Symbols.cdot, "sqrt": Symbols.Radicals.sqrt,
    "cbrt": Symbols.Radicals.cbrt, "\(1/2\)": Symbols.Fractions.half,
    "\(1/3\)": Symbols.Fractions.third, "\(1/4\)": Symbols.Fractions.fourth,
    "phi": Symbols.phi, "pi": Symbols.pi}
    for sym, val in replacements.items():
        equation = re.sub(sym, val, equation)
    return equation

def addToHistory(equation, result):
    global history
    if isNumber(result):
        if result >= 1e18:
            history.append(f"{useSymbols(equation)} = {result:e}")
        else:
            history.append(f"{useSymbols(equation)} = {result:,}")

def fixUI(userValue):
    global history
    match userValue.lower():
        case "history":
            print(*history, sep='\n')
            return None
        case "clear history":
            history = []
            return None
        case "constant" | "constants":
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

def ncr(n, r): return math.factorial(n) / ( math.factorial(r) * math.factorial(n - r) )

def npr(n, r): return math.factorial(n) / math.factorial(n - r)

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

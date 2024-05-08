from handlers._mathConstants import *
from src.mathFunctions import *
newGlobal = {
    "round": round,
    "int": int,
    "float": float,
    "bool": bool,
    "list": list,
    "dict": dict,
    "str": str,
    "abs": abs,
    "sum": sum,
    "max": max,
    "min": min,
    "pow": pow,
    "complex": complex,
    "isinstance": isinstance,
    "help": help,
    "exec": exec,
}

excludedFunctions = [
    "excludedFunctions",
    "exp2dec",
    "useSymbols",
    "addToHistory",
    "fixUI",
    "bracketMultiplication",
]

for pack in dir():
    if not pack.startswith('__') and pack not in excludedFunctions:
        newGlobal[str(pack)] = globals()[pack]
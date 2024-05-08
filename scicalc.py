#!/usr/bin/env python3

import sys
import math
import warnings
import prompt_toolkit
import re
import os
from handlers import _argHandler
from handlers._fixUi import *
from handlers._mathConstants import *
from handlers._usrConstants import *
from handlers._validators import *
from src.mathFunctions import *
from handlers._usrGlobals import newGlobal

warnings.filterwarnings("ignore")
args = vars(_argHandler.parseAndReturnArgs())
getUsrConstants(args)
sys.set_int_max_str_digits(0) # allowing very large numbers
uiSession = prompt_toolkit.PromptSession()
clear = lambda: os.system("cls" if os.name=="nt" else "clear")

while True:
    try:
        ui = uiSession.prompt(">")
        ui = re.sub(r"\s{1,}", " ", ui)
        exitAttempt = False
        match ui:
            case "" | None:
                continue
            case "clear":
                clear()
            case _:
                fixedUi = fixUi(ui)
                if fixedUi == None:
                    continue
                if DEVELOPERS:
                    result = eval(fixedUi)
                else:
                    result = eval(fixedUi, {"__builtins__": None}, newGlobal)
                allowIsNumber = type(result).__name__ != "Decimal" and type(result).__name__ != "StringedNumber"
                if EQUATION_RESULTS and type(result).__name__ != "StringedNumber":
                    print("%s = " % ui, end="")
                if isNumber(result) and allowIsNumber:
                    if float(result).is_integer():
                        result = int(result)
                    addToHistory(ui, result)
                    if result >= 1e16 and result < sys.float_info.max:
                        print(f"{result:e}")
                    else:
                        print(f"{result:,}")
                elif isinstance(result, (list, dict)):
                    addToHistory(ui, result, includeAll=True)
                    print(result)
                elif isinstance(result, complex):
                    if result.imag == 1 and result.real == 0:
                        result = 'i'
                    elif result.real == 0 and result.imag != 0:
                        result = f"{int(result.imag)}i" if result.imag.is_integer() else f"{result.imag}i"
                    else:
                        result = f"{result.real} + {result.imag}i"
                    addToHistory(ui, result, includeAll=True, includeAllWithSymbols=True)
                    print(result)
                elif isinstance(result, bool):
                    addToHistory(ui, result)
                    print(str(result).lower())
                elif type(result).__name__ in ["module", "function"]:
                    print("{}: {}".format(type(result).__name__, result.__name__))
                elif type(result).__name__ == "Decimal":
                    addToHistory(ui, str(result), includeAll=True)
                    print(result)
                elif type(result).__name__ == "StringedNumber":
                    if result.addHistory:
                        addToHistory(ui, result.num, includeAll=True)
                        print(result.num)
                    else:
                        print(result.num)
                elif result != None:
                    print(result)
    except (KeyboardInterrupt, EOFError) as ERROR:
        if type(ERROR).__name__ == "KeyboardInterrupt":
            if exitAttempt:
                raise SystemExit(0)
            exitAttempt = True
            print("Press ctrl+c again to confirm exit")
        else:
            raise SystemExit(0)
    except Exception as ERROR:
        ERROR_LINE = sys.exc_info()[-1].tb_lineno
        ERROR_TYPE = type(ERROR).__name__
        if DEVELOPERS:
            print("Exception caught on line %d: %s: %s" % (ERROR_LINE, ERROR_TYPE, ERROR))
        match ERROR_TYPE:
            case "ZeroDivisionError":
                print("undefined")
                addToHistory(ui, "undefined", includeAll=True, includeAllWithSymbols=True)
            case "OverflowError":
                print("result too big")
                addToHistory(ui, "result too big", includeAll=True, includeAllWithSymbols=True)
            case "TypeError":
                if str(ERROR) == "'NoneType' object is not subscriptable":
                    print("undefined function or variable")
                    continue
                print(ERROR)
            case _:
                print(ERROR)


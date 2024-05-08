import re
import sys
from math import inf
from handlers._mathConstants import *
from handlers import _usrConstants
from handlers._validators import *
from handlers._symbols import *

__all__ = [
    "history",
    "ans",
    "bracketMultiplication",
    "fixUi",
    "addToHistory",
    "useSymbols",
    "StringedNumber",
]

history = []
ans = ''

def bracketMultiplication(expression: str) -> str:
    expression = re.sub(r"(?<=\))(?P<num>(?:\d+?\.)?\d+)", r"*\g<num>", expression)
    expression = re.sub(r"(?P<num>(?<!\w)(?:\d+?\.)?\d+(?:(?=\()))", r"\g<num>*", expression)
    return expression

def checkFailedAutoMultiply(expression: str) -> bool:
    priorExpression = str(expression)
    subsequentExpression = bracketMultiplication(expression)
    if priorExpression != subsequentExpression:
        return True
    return False

def fixUi(userValue):
    global history, ans
    match userValue.lower():
        case "history" | "hist":
            if history != []:
                if _usrConstants.HISTORY_INDEX:
                    for index, equation in enumerate(history):
                        print(f"{len(history)-index}. {equation}")
                else:
                    print(*history, sep='\n')
            else:
                print("history is currently empty")
            return None
        case "clear history" | "clear hist":
            if history == []:
                print("history is already empty")
            history = []
            return None
        case "constant" | "constants" | "const":
            for key, value in constants.items():
                print(f"{key} = {value}")
            return None
        case "ans":
            if isinstance(ans, bool):
                print(str(ans).lower())
            else:
                print(ans)
            return None
        case "exit":
            exit()
    checkingHistory = re.search(r"^(?:history\b|hist\b)$|^(?:history\b|hist\b)\s(?P<size>\d+)$|^(?:history\b|hist\b)\s(?P<lower>\d+)\s(?P<upper>\d+)$", userValue)
    if bool(checkingHistory):
        if len(history) == 0:
            print("history is currently empty")
            return None
        if checkingHistory.group("size") != None:
            returnSize = int(checkingHistory.group("size"))
            if returnSize >= len(history): returnSize = len(history)
            if returnSize <= 0:
                raise ValueError("return size too low")
            print(*history[len(history)-returnSize:len(history)], sep='\n')
            return None
        if checkingHistory.group("lower") != None and checkingHistory.group("upper") != None:
            returnSizeLower = int(checkingHistory.group("lower"))
            returnSizeUpper = int(checkingHistory.group("upper"))
            if returnSizeLower == returnSizeUpper and 0 < returnSizeLower <= len(history):
                print(history[len(history)-returnSizeLower])
                return None
            if returnSizeLower > returnSizeUpper:
                raise ValueError("lower limit must be less than upper limit")
            if len(history) <= returnSizeLower <= 0:
                raise ValueError("lower limit out of range")
            if returnSizeUpper >= 40:
                returnSizeUpper = len(history)
            elif returnSizeUpper <= 0:
                raise ValueError("upper limit too low")
            trueUpper = len(history) - (returnSizeLower-1)
            trueLower = len(history) - returnSizeUpper
            print(*history[trueLower:trueUpper], sep='\n')
            return None
    clearingHistory = re.search(r"^(?:history|hist) (?:delete|remove) (?P<num>\d+)$|^(?:history|hist) (?:delete|remove) (?P<lower>\d+) (?P<upper>\d+)$", userValue)
    if bool(clearingHistory):
        if not bool(clearingHistory.group("lower")):
            if len(history) == 0:
                print("history is currently empty")
                return
            if int(clearingHistory.group("num")) > len(history):
                raise ValueError("history index does not exist")
            indexToDelete = len(history) - int(clearingHistory.group("num"))
            history.pop(indexToDelete)
            return
        else:
            low, up = clearingHistory.group("lower"), clearingHistory.group("upper")
            if len(history) == 0:
                print("history is currently empty")
                return
            if low >= up:
                print("lower limit must be less than upper limit")
                return
            indexFrom = len(history) - int(up)
            indexTo = len(history) - (int(low) - 1)
            valuesToRemove = history[indexFrom:indexTo]
            for i in valuesToRemove:
                history.remove(i)
            return
    userValue = re.sub(r"(?:(?<=^)|(?<=[\s\+\-\*\/\^\(\,\%]))ans(?:(?=$)|(?=[\s\+\-\*\/\^\)\,\%]))", str(ans), userValue)
    if _usrConstants.BRACKET_ASTERISK:
        userValue = bracketMultiplication(userValue)
    elif checkFailedAutoMultiply(userValue):
        print("auto multiplication is disabled")
        return
    userValue = re.sub(r'\^', "**", userValue)
    userValue = re.sub(r"\b(?P<num>\d+)i\b", r"\g<num>j", userValue)
    userValue = re.sub(r"(?:(?<=[\s\+\-\*\/\,\(])|(?:^))(?:(?P<num>\d+)!(?:(?=[\s\+\-\*\/\,\)]|(?:$))))", r"factorial(\g<num>)", userValue)
    return userValue

def addToHistory(expression, result, includeAll=False, includeAllWithSymbols=False):
    global history, ans
    if bool(re.search(r"^(?:\d+\.\d+|\.\d+|\d+)$", expression)):
        return
    if isNumber(result) and isinstance(result, (int, float)):
        # remove last equation from history if the max. limit is reached
        if len(history) >= 40:
            history.pop(0)
        if result >= 1e16 and result < sys.float_info.max:
            appendText = f"{useSymbols(expression)} = {result:e}"
            if result == inf:
                appendText = f"{useSymbols(expression)} = {useSymbols(result)}"
            if appendText in history:
                history.remove(appendText)
            history.append(appendText)
        else:
            appendText = f"{useSymbols(expression)} = {result:,}"
            if result == inf:
                appendText = f"{useSymbols(expression)} = {useSymbols(result)}"
            if appendText in history:
                history.remove(appendText)
            history.append(appendText)
        ans = result
    elif isinstance(result, complex):
        if len(history) >= 40:
            history.pop(0)
        ans = result
        if result.real == 0:
            result = "{}i".format(result.imag)
        else:
            result = "{} + {}i".format(result.real, result.imag)
        appendText = f"{useSymbols(expression)} = {result}"
        if appendText in history:
            history.remove(appendText)
        history.append(appendText)
    elif isinstance(result, list):
        if len(history) >= 40:
            history.pop(0)
        ans = result
        appendText = f"{useSymbols(expression)} = {result}"
        if appendText in history:
            history.remove(appendText)
        history.append(appendText)
    elif isinstance(result, bool):
        if len(history) >= 40:
            history.pop(0)
        ans = result
        result = str(result).lower()
        appendText = f"{useSymbols(expression)} = {result}"
        if appendText in history:
            history.remove(appendText)
        history.append(appendText)
    elif includeAll:
        if len(history) >= 40:
            history.pop(0)
        if includeAllWithSymbols:
            expression = useSymbols(expression)
        appendText = f"{expression} = {result}"
        if appendText in history:
            history.remove(appendText)
        history.append(appendText)
        ans = result

def useSymbols(expression):
    if not _usrConstants.USE_SYMBOLS:
        return expression
    expression = str(expression)
    replacements = {
        r"\*": mathSymbols['cdot'],
        r"(?<!.)\bsqrt\((?P<num>\d+)\)": rf"{mathSymbols['sqrt']}\g<num>",
        r"(?<!\.)\bsqrt": mathSymbols['sqrt'],
        r"(?<!\.)\bcbrt": mathSymbols['cbrt'],
        r"(?:(?:(?<=[\+\-\*\/\,\(\^\s])|\A)\(1/2\)(?:(?=(?:[\+\-\*\/\,\)\^\s]|\Z))))": mathSymbols['half'],
        r"(?:(?:(?<=[\+\-\*\/\,\(\^\s])|\A)\(1/4\)(?:(?=(?:[\+\-\*\/\,\)\^\s]|\Z))))": mathSymbols['fourth'],
        r"(?:(?:(?<=[\+\-\*\/\,\(\^\s])|\A)\(3/4\)(?:(?=(?:[\+\-\*\/\,\)\^\s]|\Z))))": mathSymbols['quarter3'],
        r"(?:(?<=^)|(?<=[\s\+\-\*\/|\^|\(|\,]))phi(?:(?=$)|(?=[\s\+\-\*\/\|\^|\)|\,]))": mathSymbols['phi'],
        r"(?:(?<=^)|(?<=[\s\+\-\*\/|\^|\(|\,]))pi(?:(?=$)|(?=[\s\+\-\*\/\|\^|\)|\,]))": mathSymbols['pi'],
        r"/": mathSymbols['divide'],
        r"(?:(?<=^)|(?<=[\s\+\-\*\/|\^|\(|\,]))(infinity|inf)(?:(?=$)|(?=[\s\+\-\*\/\|\^|\)|\,]))": mathSymbols['infinity'],
        r"\babs\((?P<expression>[^\(\)]*[^\(\)])\)": r"|\g<expression>|",
        r"(?<!\.)(\bfact|\bfactorial|^fact|^factorial)\((?P<num>\d+)\)(?!\S)": r"(\g<num>)!",
    }
    for sym, val in replacements.items():
        expression = re.sub(sym, val, expression)
    return expression

class StringedNumber:
    def __init__(self, num, returnAsInt=False, addHistory=True):
        self.addHistory = addHistory
        if returnAsInt:
            self.num = int(num)
        else:
            self.num = str(num)

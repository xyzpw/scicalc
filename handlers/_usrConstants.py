__all__ = [
    "HISTORY_INDEX",
    "BRACKET_ASTERISK",
    "DEVELOPERS",
    "EQUATION_RESULTS",
    "USE_SYMBOLS",
    "getUsrConstants",
]

HISTORY_INDEX = False
BRACKET_ASTERISK = True
DEVELOPERS = False
EQUATION_RESULTS = False
USE_SYMBOLS = True
def getUsrConstants(usrArgs: dict):
    global HISTORY_INDEX, BRACKET_ASTERISK, DEVELOPERS, EQUATION_RESULTS, USE_SYMBOLS
    HISTORY_INDEX = usrArgs.get("history_index")
    BRACKET_ASTERISK = not usrArgs.get("no_auto_multiply")
    DEVELOPERS = usrArgs.get("developer")
    EQUATION_RESULTS = usrArgs.get("equation_results")
    USE_SYMBOLS = not usrArgs.get("no_symbols")
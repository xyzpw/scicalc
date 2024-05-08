from argparse import ArgumentParser

parser = ArgumentParser()

def addBoolArgs(argName: str, argDesc: str):
    parser.add_argument(argName, help=argDesc, action="store_true")

# creates terminal arguments
def parseAndReturnArgs():
    addBoolArgs("--no-symbols", "disables mathematical symbols in history")
    addBoolArgs("--no-auto-multiply", "disables auto multiplication between brackets")
    addBoolArgs("--equation-history", "results are displayed as an equation")
    addBoolArgs("--history-index", "displays index of each history item adjacent to their values")
    addBoolArgs("--developer", "enables developer mode")
    return parser.parse_args()



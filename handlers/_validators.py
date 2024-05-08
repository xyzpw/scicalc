__all__ = [
    "isNumber",
]

def isNumber(value):
    if isinstance(value, bool):
        return False
    if str(value).isnumeric():
        return True
    else:
        try:
            value = float(value)
            return True
        except:
            return False

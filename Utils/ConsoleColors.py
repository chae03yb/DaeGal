# For Linux

class EFCT():
    CLEAR = "\033[0m"
    BOLD = "\033[1m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    STRIKEOUT = "\033[9m"

class TEXT():
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33"
    BLUE = "\033[34m"
    PURPLE = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    Bright = "\033[90m"
    BrightRed = "\033[91m"
    BrightGreen = "\033[92m"
    BrightYellow = "\033[93m"
    BrightBlue = "\033[94m"
    BrightPurple = "\033[95m"
    BrightCyan = "\033[96m"
    BrightWhite = "\033[97m"

class BG():
    BLACK = "\033[40m"
    RED = "\033[41m"
    GREEN = "\033[42m"
    YELLOW = "\033[43m"
    BLUE = "\033[44m"
    PURPLE = "\033[45m"
    CYAN = "\033[46m"
    WHITE = "\033[47m"

    BrightBlack = "\033[100m"
    BrightRed = "\033[101m"
    BrightGreen = "\033[102m"
    BrightYellow = "\033[103m"
    BrightBlue = "\033[104m"
    BrightPurple = "\033[105m"
    BrightCyan = "\033[107m"
    BrightWhite = "\033[108m"

def TEXT_8Bit(Num:int):
    return f"\033[38;5;{Num}m"

def BG_8Bit(Num:int):
    return f"\033[48;5;{Num}m"

def TEXT_RGB(R:int, G:int, B:int):
    return f"\033[38;2;{R};{G};{B}m"

def BG_RGB(R:int, G:int, B:int):
    return f"\033[48;2;{R};{G};{B}m"
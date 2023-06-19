import time

class bcolors:
    DEFAULT = "\033[0m"
    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[0;33m"
    BLUE = "\033[0;34m"
    MAGENTA = "\033[0;35m"
    CYAN = "\033[0;36m"
    WHITE = "\033[0;37m"
    BRIGHT_BLACK = "\033[0;90m"
    BRIGHT_RED = "\033[0;91m"
    BRIGHT_GREEN = "\033[0;92m"
    BRIGHT_YELLOW = "\033[0;93m"
    BRIGHT_BLUE = "\033[0;94m"
    BRIGHT_MAGENTA = "\033[0;95m"
    BRIGHT_CYAN = "\033[0;96m"
    BRIGHT_WHITE = "\033[0;97m"
    BOLD = "\033[1m"

class unicode:
    CHECKMARK = "\u2713"
    CROSS = "\u2717"


def _timer(func):
    def wrapper(*args):
        start = time.ticks_ms()
        func(*args)
        delta = time.ticks_ms() - start
        print(f' {bcolors.YELLOW}({delta}ms){bcolors.WHITE}')
    return wrapper


class Test:
    def __init__(self, name):
        self.name = name

    @_timer
    def assert_equal(self, test, expected):
        print(f"{bcolors    .WHITE}{self.name} : ", end="")
        if test==expected:
            print(f'{bcolors.GREEN} PASSED', end="")
        else:
            print(f'{bcolors.RED} FAILED ({test} but expected {expected})', end="")

    @_timer
    def assert_not_equal(self, test, expected):
        print(f"{bcolors    .WHITE}{self.name} : ", end="")
        if test!=expected:
            print(f'{bcolors.GREEN} PASSED', end="")
        else:
            print(f'{bcolors.RED} FAILED ({test} but expected something different than {expected})', end="")

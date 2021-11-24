import sys
import time as t


if len(sys.argv) > 1:
    modelPath = str(sys.argv[1])
else:
	modelPath = 'cnf.txt'

cykParser.getCNF(modelPath)

inputFile = input("Masukkkan path file python: ")
if inputFile:
    t1 = time.perf_counter()

    lxr = Lexer.Lexer()
    lxr.lex_file(inputFile)
    tokenValues = list(map(lambda t: t.value, lxr.tokens))
    t2 = time.perf_counter()
    print(f"Done in {t2 - t1}s", end="\n\n")

class LexState(Enum):
    START = auto()
    ZERO = auto()
    HEX = auto()
    BIN = auto()
    OCT = auto()
    STR = auto()
    STR3 = auto()
    SQUOTE = auto()
    SQUOTE1 = auto()
    SQUOTE2 = auto()



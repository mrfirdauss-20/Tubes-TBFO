import sys
import time as t

import cykParser
import Lexer

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

    if cykParser.cykParser(tokenValues):
        print("Accepted.")
    else:
        print("Syntax Error.")

    t2 = time.perf_counter()
    print(f"Done in {t2 - t1}s", end="\n\n")

class LexState(Enum):
    START = auto()
    ZERO = auto()
    HEX = auto()
    BIN = auto()
    OCT = auto()
    ALPHA = auto()
    DIGIT = auto()
    ALNUM = auto()
    SYMBOL = auto()
    BLANK = auto()
    NUM = auto()
    XBONUM = auto()
    WORD = auto()
    STR = auto()
    STR3 = auto()
    SQUOTE = auto()
    SQUOTE1 = auto()
    SQUOTE2 = auto()
    SQUOTE3 = auto()
    SQUOTE32 = auto()
    SQUOTE31 = auto()
    DQUOTE = auto()
    DQUOTE1 = auto()
    DQUOTE2 = auto()
    DQUOTE3 = auto()
    DQUOTE32 = auto()
    DQUOTE31 = auto()
    COMMENT = auto()
    BACKSLASH = auto()
    ILLEGAL = auto()


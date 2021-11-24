import sys
import time

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

    if Lexer.Token.ILLEGAL not in lxr.tokens and cykParser.cykParser(tokenValues):
        print("Accepted.")
    else:
        print("Syntax Error.")

    t2 = time.perf_counter()
    print(f"Done in {t2 - t1}s", end="\n\n")

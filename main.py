import cykParser
import sys
import Lexer

if len(sys.argv) > 1:
    modelPath = str(sys.argv[1])
else:
	modelPath = 'cnf.txt'

cykParser.getCNF(modelPath)

inputFile = input("Masukkkan path file python: ")
if inputFile:
    lxr = Lexer.Lexer()
    lxr.lex_file(inputFile)
    tokenValues = list(map(lambda t: t.value, lxr.tokens))
    cykParser.cykParser(tokenValues)

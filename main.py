import cykParser
import sys
import Lexerr

if len(sys.argv) > 1:
    modelPath = str(sys.argv[1])
else:
	modelPath = 'cnf1_fikron.txt'
#load CNF to dictionary	
cykParser.getCNF(modelPath)


# inputFile = input("Masukkkan nama file yang ingin di-lexing: ")
lexer = Lexerr.Lexer()
with open("tes.py") as f:
    for ln in f:
        lexer.lex(ln + "\n")
    last = None
    for token in lexer.tokens:
        if token == Lexerr.Token.NL:
            if last != Lexerr.Token.NL:
                print("")
        else:
            print(token.value, end=" ")
        last = token
i = map(lambda x: x.value, lexer.tokens)
# for y in i:
#     if y in cykParser.CNF:
#         print(y, cykParser.CNF[y])
tes = []
# i = i.split(" ")
i = [string for string in i if string != ""]
# print(i)
# print(i.count("NEWLINE"))
j = 1

# for x in i:
#     print(x, end=" ")
#     if x == "NEWLINE":
#         print(j)
#         j += 1

#start parsing
cykParser.cykParser(i)
# print(i)
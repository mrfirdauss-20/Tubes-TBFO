import LexerFunc
import sys
import cykParser


# Load Chomsky Normal Form
if len(sys.argv) > 1:
    modelPath = str(sys.argv[1])
else:
	modelPath = 'cnf1_fikron.txt'
	
cykParser.getCNF(modelPath)

tokenized= LexerFunc.startToken("input_fikron.txt")
i=tokenized
tes=[]
# i=i.split(' ')
i = [string for string in i if string !='']

print(i)
# print(len(i))
cykParser.cykParser(i)

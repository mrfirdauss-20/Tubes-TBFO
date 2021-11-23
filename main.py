import LexerFunc
import cfg2cnf

inputFile = input('Masukkkan nama file yang ingin di-lexing: ')
tokenized= LexerFunc.startToken(inputFile)

print(tokenized)
import LexerFunc

inputFile = input('Masukkkan nama file yang ingin di-lexing: ')
tokenized= LexerFunc.startToken(inputFile)
print(tokenized)
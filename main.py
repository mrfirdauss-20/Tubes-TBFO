import abc
import LexerFunc
import cfg2cnf

inputFile = input('Masukkkan nama file yang ingin di-lexing: ')
tokenized= LexerFunc.startToken(inputFile)
i=tokenized
tes=[]
i=i.split(' ')
i = [string for string in i if string !='']

print(i)

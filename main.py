import LexerFunc

inputFile = input("Masukkkan nama file yang ingin di-lexing: ")
tokenized = LexerFunc.startToken(inputFile)
i = tokenized
tes = []
i = i.split(" ")
i = [string for string in i if string != ""]

print(i.count("NEWLINE"))
j = 1

for x in i:
    print(x, end=" ")
    if x == "NEWLINE":
        print(j)
        j += 1

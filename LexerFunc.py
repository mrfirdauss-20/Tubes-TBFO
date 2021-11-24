import re
import lexRules


def initRules(rules):
# I.S. sebuah rules dari pembacaan regecx menuju non-terminal dalam bentuk array of set pasangan regex dan nonterminal
# F.S. string compile regex dan pasangan key value group regex dan nonterminal
    rulesNo = 1
    regexList =[] #ini buat nyimpen regexnya dalam bentuk list, biar bisa langsung di -join- ke dalam array
    nonTerminalDict ={} #buat nyimpen key and value regex ke non terminal

    for regex, nonTerminal in rules:
        groupName= 'GROUP{}'.format(rulesNo)
        regexList.append('(?P<{}>{})'.format(groupName,regex))
        nonTerminalDict[groupName]=nonTerminal
        rulesNo+=1
    
    regex = re.compile('|'.join(regexList)) #string regex dengan model "re(1) | re(2)" ...
    #re_ignoreBlank = re.compile('\S')

    return regex,nonTerminalDict

def tokenizer(buffer,idx, isIgnoreBlank,regexString, nonTerminalDict):
    #I.S. terdefinisi
    #F.S. mengembalikan none jika sudah habis pembacaan dari sebuah textr
    #dan mengembalikan sebuah nonterminal dari sebuah potongan program
    if idx>= len(buffer):
        return None,idx
    else:
        if(isIgnoreBlank):
            ignoreBlankRegex =  re.compile('\S')
            compiler = ignoreBlankRegex.search(buffer,idx) #mencari non blank setalh elemen ke idx

            if compiler: #jika ditemukan lagi non blank dalam buffer
                idx=compiler.start()
            else:
                return None,idx
        
        compiler = regexString.match(buffer,idx)

        if compiler:
            getRegexGroup = compiler.lastgroup
            nonTerminal = nonTerminalDict[getRegexGroup]
            idx=compiler.end()
            #print(idx, nonTerminal)
            return nonTerminal,idx
    

def tokening(buffer, idx,regexString, nonTerminalDict):
    #I.S. terdefinisi
    #F.S. mengembalikan berkali-kali untuk tiap token dari tiap komponen nonterminal
    nonTerminal= 'START'
    while(nonTerminal!=None):
        nonTerminal,idx=tokenizer(buffer, idx, False, regexString,nonTerminalDict)
        #print(nonTerminal,idx)
        yield nonTerminal


def startToken(inputFile):
    #I.S. masukan sebuha strijng terdefinisi nama file
    #F.S. mengemablikan sebuhah file yang sudah ditokenized
    filePath = './' + inputFile

    f = open(filePath,'r')
    text = f.read()
    #print(text)
    reString, nonTerDict = initRules (lexRules.conversion)
    output=''
    idx=0
    try:
        for token in tokening(text,idx,reString,nonTerDict):
            if token != 'BLANK' and token != None:
                output+=token+' '
            
    except:
        print("Error when lexing file")
    
    #print(output)
    i=output.split(' ')
    i = [string for string in i if string !='']

    return i


    


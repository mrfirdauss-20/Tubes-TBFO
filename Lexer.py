import lexRules
import re

class LexerError(Exception):
    def __init__(self,pos) :
        self.pos=pos

class Lexer(object):
    def __init__(self, rules, ignoreBlank):
        countRules=1
        regexList = []
        self.dictType={}

        for regex, terminal in rules:
            groupName= 'GROUP{}'.format(countRules)
            regexList.append('(?P<{}>{})'.format(groupName, regex))
            self.dictType[groupName]=terminal
            countRules+=1
        
        self.regex=re.compile('|'.join(regexList))
        self.ignoreBlank = ignoreBlank
        self.re_ignoreBlank = re.compile('\S')

    def input(self,buf):
        self.buf=buf
        self.id=0
    
    def tokenizer(self):
        if(self.id)>= len(self.buf):
            return None
        else:
            if self.ignoreBlank:
                compiler = self.re_ignoreBlank.search(self.buf, self.id)

                if compiler:
                    self.id = compiler.start()
                else:
                    return None
            compiler = self.regex.match(self.buf,self.id)
            if compiler:
                catchGroup = compiler.lastgroup
                nonTerminal = self.dictType[catchGroup]
                self.id = compiler.end()
                return nonTerminal
    
    def tokening(self):
        nonTerminal = 'START'
        while(nonTerminal!=None):
            nonTerminal = self.tokenizer()
            yield nonTerminal

input_file = input("Input file to check : ")
lx = Lexer(rules=lexRules.conversion,ignoreBlank=True)
file_path = './' + input_file
file = open(file_path, 'r')
text = file.read()
lx.input(text)
output=''
print(lx.tokening())

try:
    for word in lx.tokening():
        if word!='BLANK' and word!=None :
            output+=word + ' '
except LexerError as err:
    print('LexerError at position {}'.format(err.pos))
print(output)
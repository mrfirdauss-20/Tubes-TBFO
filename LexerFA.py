from tokens import *

def isLetter(ch):
    return ("a"<=ch and ch<="z") or  ("A"<= ch and ch<="Z" ) or ('_'==ch)

def isBlank(ch):
    return ch==' ' or ch=='\t' or ch == '\r'

def isNum(ch):
    return ("0"<=ch and ch<="9") or ch=='.'



class Lexer(object):
    def __init__(self, input_data) -> None:
        self.buffer = input_data
        self.pos =0
        self.ch=''
        self.adv()
    
    def adv(self):
        if(self.pos>=len(self.buffer)):
            self.ch="\x00"
        else:
            self.ch = self.buffer[self.pos]
        
        self.pos+=1
    
    def lexEoT(self):
        if self.ch=='\x00':
            return TokenInfo(EOF, self.ch)
        
    def ignoreBlank(self):
        while(isBlank(self.ch)):
            self.adv()
    
    def lexOperator(self):
        switcher = {  
        "+": Token.PLUS,    "-": Token.MINUS,   "/": Token.DIVIDE,  "*": Token.MULTIPLY,
       "%": Token.MOD, "=": Token.EQUALS,  "!": Token.EXP, '#': Token.Sharp, '\n': Token.NL,
       "|": Token.OR,      "&": Token.AND,     ",": Token.COMMA,   ";": Token.SEMICOLON,  
       "(": Token.LP,  ")": Token.RP,  "{": Token.LBRACE,  "}": Token.RBRACE,     
       "[": Token.LB, "]": Token.RB, "<": Token.SMALESSLL,   ">": Token.GREATER,
       "\&": Token.AMP,
        }

        double_switcher={
            "==": Token.ISEQ, "!=": Token.NEQ, "->": Token.RARROW, "**": Token.POW, "\\": Token.DOUBLE,
            ">=":Token.GE,"<=":Token.LE,"!=": Token.NOT_EQUAL,
        }

        if tok := switcher.get(self.ch,None):
            ch=self.ch
            self.adv()

            if(newTok:=double_switcher.get(ch+self.ch,None)):
                tok=newTok
                ch+=self.ch
                self.adv()

            return TokenInfo(tok.name,ch)


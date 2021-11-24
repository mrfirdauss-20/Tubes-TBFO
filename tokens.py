from collections import namedtuple
from enum import Enum

class NewEnum(Enum):
    def __eq__(self,b):
        if(isinstance(b,str)):
            print(2)
            return self.name==b
        else:
            return self.name==b.name

    def __hash__(self):
        return id(self.name)

TokenInfo = namedtuple('TokenInfo', ['name', 'value'])

EOF ="EOF"
ILLEGAL = 'ILLEGAL'

Token = NewEnum('Token', [ 

])

keywords ={
    "def": Token.DEF.name,
    "if"    : Token.IF.name,
    "else"  : Token.ELSE.name,
    "True"  : Token.TRUE.name,
    "False" : Token.FALSE.name,
    "return": Token.RETURN.name,
    "print" : Token.PRINT.name,
    "while" : Token.WHILE.name,
    "for"   : Token.FOR.name,
    "in"    : Token.IN.name,
    "break" : Token.BREAK.name,
    "continue": Token.CONTINUE.name,
    "range" : Token.RANGE.name,
    "is": Token.IS.name,
    "as" : Token.AS.name,
    "class": Token.CLASS.name,
    "raise": Token.RAISE.name,
    "None":Token.NONE.name,
    "elif": Token.ELIF.name,
    "from": Token.FROM.name,
    "import": Token.IMPORT.name,
    "or":Token.OR.name,
    "and":Token.AND.name,
    "not": Token.NOT.name,
    "with":Token.WITH.name,
    "\'\'\'": Token.TRIPLEQ.name,
    "\"\"\"": Token.TRIPLEQ.name,
}


def get_token(data):
    return keywords.get(data, Token.ID.name)

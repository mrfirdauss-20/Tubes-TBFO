from enum import Enum, auto


def is_alpha(ch: str):
    return ("a" <= ch and ch <= "z") or ("A" <= ch and ch <= "Z") or ("_" == ch)


def is_digit(ch: str):
    return "0" <= ch and ch <= "9"


def is_hex(ch: str):
    return ("0" <= ch and ch <= "9") or ("A" <= ch and ch <= "F")


def is_oct(ch: str):
    return "0" <= ch and ch <= "7"


def is_bin(ch: str):
    return ch == "0" or ch == "1"


def is_space(ch: str):
    return ch in [" ", "\t", "\n", "\v", "\f", "\r"]


class LexState(Enum):
    START = auto()
    ZERO = auto()
    HEX = auto()
    BIN = auto()
    OCT = auto()
    ALPHA = auto()
    DIGIT = auto()
    ALNUM = auto()
    SYMBOL = auto()
    BLANK = auto()
    NUM = auto()
    XBONUM = auto()
    WORD = auto()
    STR = auto()
    STR3 = auto()
    SQUOTE = auto()
    SQUOTE2 = auto()
    SQUOTE3 = auto()
    SQUOTE32 = auto()
    SQUOTE31 = auto()
    DQUOTE = auto()
    DQUOTE1 = auto()
    DQUOTE2 = auto()
    DQUOTE3 = auto()
    DQUOTE32 = auto()
    DQUOTE31 = auto()
    COMMENT = auto()
    BACKSLASH = auto()
    ILLEGAL = auto()


class LexInput(Enum):
    START = auto()
    ZERO = auto()
    LETTERX = auto()
    LETTERB = auto()
    LETTERO = auto()
    HEX = auto()
    BIN = auto()
    OCT = auto()
    DIGIT = auto()
    ALPHA = auto()
    SHARP = auto()
    SQUOTE = auto()
    DQUOTE = auto()
    BACKSLASH = auto()
    NEWLINE = auto()
    SYMBOL = auto()
    BLANK = auto()
    NOSQUOTE = auto()
    NODQUOTE = auto()
    UNKNOWN = auto()


class Token(Enum):
    # Keywords

    TRUE = "true"
    FALSE = "false"
    NONE = "none"
    AND = "and"
    IS = "is"
    NOT = "not"
    IN = "in"
    WITH = "with"
    AS = "as"
    BREAK = "break"
    CLASS = "class"
    CONTINUE = "cont"
    DEF = "def"
    IF = "if"
    ELIF = "elif"
    ELSE = "else"
    FOR = "for"
    WHILE = "while"
    FROM = "from"
    IMPORT = "import"
    RAISE = "raise"
    RETURN = "return"

    # Operators

    LP = "lp"
    RP = "rp"
    LB = "lb"
    RB = "rb"
    LC = "lc"
    RC = "rc"
    COLON = "colon"
    DOT = "dot"
    COMMA = "comma"
    SHARP = "sharp"
    TILDE = "tilde"
    MULT = "mult"
    DIV = "div"
    MOD = "mod"
    PLUS = "plus"
    MIN = "min"
    AMP = "amp"
    BNOT = "bnot"
    BOR = "bor"
    EXC = "exc"
    GT = "gt"
    LT = "lt"
    EQ = "eq"

    # Other

    COMMENT = "comment"
    NUM = "int"
    XBO = "xbo"
    STR = "str"
    ID = "id"
    NL = "nl"
    UNDEF = "undef"

    # Special value

    ILLEGAL = "illegal"


class Lexer:
    symbols = "( ) [ ] { } : . , # ~ * / % + - < > & ^ | = ! \n".split(" ")

    keywords = {
        "True": Token.TRUE,
        "False": Token.FALSE,
        "None": Token.NONE,
        "and": Token.AND,
        "is": Token.IS,
        "not": Token.NOT,
        "in": Token.IN,
        "with": Token.WITH,
        "break": Token.BREAK,
        "class": Token.CLASS,
        "continue": Token.CONTINUE,
        "def": Token.DEF,
        "if": Token.IF,
        "elif": Token.ELIF,
        "else": Token.ELSE,
        "for": Token.FOR,
        "while": Token.WHILE,
        "from": Token.FROM,
        "import": Token.IMPORT,
        "raise": Token.RAISE,
        "return": Token.RETURN,
    }

    operators = {
        "(": Token.LP,
        ")": Token.RP,
        "[": Token.LB,
        "]": Token.RB,
        "{": Token.LC,
        "}": Token.RC,
        ":": Token.COLON,
        ".": Token.DOT,
        ",": Token.COMMA,
        "#": Token.SHARP,
        "~": Token.TILDE,
        "*": Token.MULT,
        "/": Token.DIV,
        "%": Token.MOD,
        "+": Token.PLUS,
        "-": Token.MIN,
        "&": Token.AMP,
        "^": Token.BNOT,
        "|": Token.BOR,
        "!": Token.EXC,
        ">": Token.GT,
        "<": Token.LT,
        "=": Token.EQ,
        "\n": Token.NL,
    }

    transtable = {
        LexState.START: {
            LexInput.ZERO: LexState.ZERO,
            LexInput.ALPHA: LexState.ALPHA,
            LexInput.DIGIT: LexState.DIGIT,
            LexInput.DQUOTE: LexState.DQUOTE1,
            LexInput.SHARP: LexState.COMMENT,
            LexInput.BACKSLASH: LexState.BACKSLASH,
            LexInput.SYMBOL: LexState.SYMBOL,
            LexInput.BLANK: LexState.BLANK,
            LexInput.UNKNOWN: LexState.START,
        },
        LexState.ALPHA: {
            LexInput.ALPHA: LexState.ALPHA,
            LexInput.DIGIT: LexState.ALNUM,
            LexInput.SYMBOL: LexState.WORD,
            LexInput.BLANK: LexState.WORD,
            LexInput.BACKSLASH: LexState.BACKSLASH,
        },
        LexState.ALNUM: {
            LexInput.ALPHA: LexState.ILLEGAL,
            LexInput.DIGIT: LexState.ALNUM,
            LexInput.SYMBOL: LexState.WORD,
            LexInput.BLANK: LexState.WORD,
            LexInput.BACKSLASH: LexState.BACKSLASH,
        },
        LexState.ZERO: {
            LexInput.LETTERX: LexState.HEX,
            LexInput.LETTERB: LexState.BIN,
            LexInput.LETTERO: LexState.OCT,
            LexInput.ALPHA: LexState.ILLEGAL,
            LexInput.DIGIT: LexState.DIGIT,
            LexInput.SYMBOL: LexState.WORD,
            LexInput.BLANK: LexState.WORD,
            LexInput.ZERO: LexState.DIGIT,
            LexInput.BACKSLASH: LexState.BACKSLASH,
        },
        LexState.DIGIT: {
            LexInput.ALPHA: LexState.ILLEGAL,
            LexInput.DIGIT: LexState.DIGIT,
            LexInput.SYMBOL: LexState.NUM,
            LexInput.BLANK: LexState.NUM,
            LexInput.BACKSLASH: LexState.BACKSLASH,
        },
        LexState.HEX: {
            LexInput.HEX: LexState.HEX,
            LexInput.SYMBOL: LexState.XBONUM,
            LexInput.BLANK: LexState.XBONUM,
            LexInput.BACKSLASH: LexState.BACKSLASH,
        },
        LexState.BIN: {
            LexInput.BIN: LexState.BIN,
            LexInput.SYMBOL: LexState.XBONUM,
            LexInput.BLANK: LexState.XBONUM,
            LexInput.BACKSLASH: LexState.BACKSLASH,
        },
        LexState.OCT: {
            LexInput.OCT: LexState.OCT,
            LexInput.SYMBOL: LexState.XBONUM,
            LexInput.BLANK: LexState.XBONUM,
            LexInput.BACKSLASH: LexState.BACKSLASH,
        },
        LexState.DQUOTE: {
            LexInput.DQUOTE: LexState.STR,
            LexInput.NEWLINE: LexState.ILLEGAL,
            LexInput.NODQUOTE: LexState.DQUOTE,
        },
        LexState.DQUOTE1: {
            LexInput.DQUOTE: LexState.DQUOTE2,
            LexInput.NEWLINE: LexState.ILLEGAL,
            LexInput.NODQUOTE: LexState.DQUOTE,
        },
        LexState.DQUOTE2: {
            LexInput.DQUOTE: LexState.DQUOTE3,
            LexInput.NEWLINE: LexState.ILLEGAL,
            LexInput.NODQUOTE: LexState.STR,
        },
        LexState.DQUOTE3: {
            LexInput.NODQUOTE: LexState.DQUOTE3,
            LexInput.NEWLINE: LexState.DQUOTE3,
            LexInput.DQUOTE: LexState.DQUOTE32,
        },
        LexState.DQUOTE32: {
            LexInput.NODQUOTE: LexState.DQUOTE3,
            LexInput.NEWLINE: LexState.DQUOTE3,
            LexInput.DQUOTE: LexState.DQUOTE31,
        },
        LexState.DQUOTE31: {
            LexInput.NODQUOTE: LexState.DQUOTE3,
            LexInput.NEWLINE: LexState.DQUOTE3,
            LexInput.DQUOTE: LexState.STR,
        },
        LexState.COMMENT: {
            LexInput.UNKNOWN: LexState.COMMENT,
            LexInput.NEWLINE: LexState.START,
        },
        LexState.BACKSLASH: {
            LexInput.NEWLINE: LexState.START,
        },
    }

    tokens = []

    def parse_char(self, char: str, start: LexInput):
        if char == "0" and start.value < LexInput.ZERO.value:
            return LexInput.ZERO
        elif char == "x" and start.value < LexInput.LETTERX.value:
            return LexInput.LETTERX
        elif char == "b" and start.value < LexInput.LETTERB.value:
            return LexInput.LETTERB
        elif char == "o" and start.value < LexInput.LETTERO.value:
            return LexInput.LETTERO
        elif is_hex(char) and start.value < LexInput.HEX.value:
            return LexInput.HEX
        elif is_bin(char) and start.value < LexInput.BIN.value:
            return LexInput.BIN
        elif is_oct(char) and start.value < LexInput.OCT.value:
            return LexInput.OCT
        elif is_digit(char) and start.value < LexInput.DIGIT.value:
            return LexInput.DIGIT
        elif is_alpha(char) and start.value < LexInput.ALPHA.value:
            return LexInput.ALPHA
        elif char == "'" and start.value < LexInput.SQUOTE.value:
            return LexInput.SQUOTE
        elif char == '"' and start.value < LexInput.DQUOTE.value:
            return LexInput.DQUOTE
        elif char == "#" and start.value < LexInput.SHARP.value:
            return LexInput.SHARP
        elif char == "\\" and start.value < LexInput.BACKSLASH.value:
            return LexInput.BACKSLASH
        elif char == "\n" and start.value < LexInput.NEWLINE.value:
            return LexInput.NEWLINE
        elif char in self.symbols and start.value < LexInput.SYMBOL.value:
            return LexInput.SYMBOL
        elif is_space(char) and start.value < LexInput.BLANK.value:
            return LexInput.BLANK
        elif char not in ["'", "\n"] and start.value < LexInput.NOSQUOTE.value:
            return LexInput.NOSQUOTE
        elif char not in ['"', "\n"] and start.value < LexInput.NODQUOTE.value:
            return LexInput.NODQUOTE

        return LexInput.UNKNOWN

    def delta(self, state: LexState, input: LexInput):
        if input in self.transtable[state]:
            return self.transtable[state][input]
        return LexState.ILLEGAL

    def lex(self, string: str):
        string += " "
        state = LexState.START
        word = ""

        while string:
            inp = LexInput.START
            char = string[0]

            word += char

            while string:
                inp = self.parse_char(char, inp)
                nextState = self.delta(state, inp)
                # print(char, inp, state, nextState)

                if nextState != LexState.ILLEGAL or inp == LexInput.UNKNOWN:
                    break

            if nextState in [
                LexState.WORD,
                LexState.XBONUM,
                LexState.NUM,
                LexState.STR,
            ]:
                word = word[:-1]

            if nextState == LexState.SYMBOL:
                if char in self.operators:
                    self.tokens.append(self.operators[char])
                else:
                    self.tokens.append(Token.UNDEF)
                state = nextState
                nextState = LexState.START
            elif nextState == LexState.WORD:
                if word in self.keywords:
                    self.tokens.append(self.keywords[word])
                else:
                    self.tokens.append(Token.ID)
                state = nextState
                nextState = LexState.START
            elif nextState == LexState.XBONUM:
                self.tokens.append(Token.XBO)
                state = nextState
                nextState = LexState.START
            elif nextState == LexState.NUM:
                self.tokens.append(Token.NUM)
                state = nextState
                nextState = LexState.START
            elif nextState in [LexState.STR, LexState.STR3]:
                self.tokens.append(Token.STR)
                state = nextState
                nextState = LexState.START

            if nextState == LexState.ILLEGAL:
                self.tokens.append(Token.ILLEGAL)
                nextState = LexState.START
            elif nextState == LexState.BLANK:
                nextState = LexState.START

            if nextState == LexState.START:
                word = ""
                if state in [
                    LexState.WORD,
                    LexState.XBONUM,
                    LexState.NUM,
                ]:
                    if not is_space(char):
                        string = char + string

            state = nextState
            string = string[1:]

        if state not in [
            LexState.START,
            LexState.SYMBOL,
            LexState.WORD,
            LexState.XBONUM,
            LexState.NUM,
            LexState.STR,
            LexState.STR3,
            LexState.COMMENT,
            LexState.BLANK,
        ]:
            self.tokens.append(Token.ILLEGAL)

def startLexerr(fileName):
    lexer =Lexer()
    with open(fileName) as f:
        for ln in f:
            lexer.lex(ln+"\n")
        
    print(lexer.tokens)
if __name__ == "__main__":
    lexer = Lexer()
    with open("main.py") as f:
        for ln in f:
            lexer.lex(ln + "\n")
    last = None
    for token in lexer.tokens:
        if token == Token.NL:
            if last != Token.NL:
                print("")
        else:
            print(token.value, end=" ")
        last = token

    startLexerr("main.py")
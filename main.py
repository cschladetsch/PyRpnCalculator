# vi: set expandtab tabstop=4 shiftwidth=4 softtabstop=4:

from enum import Enum

class TokenType(Enum):
    Null = 0

    Plus = 2
    Minus = 3
    Mul = 4
    Div = 5

    Number = 10
    String = 11
    Vector = 12
    Map = 13

    Assert = 30

    Dup = 40
    Over = 41
    Swap = 42
    Roll = 43
    Rot = 44
    Depth = 45

    Store = 50

    Ident = 60
    QuotedIdent = 61

    ToVec = 70
    ToString = 71
    ToMap = 72
    ToSet = 73
    Expand = 74
    ToVec3 = 75
    ToVec4 = 76

    If = 90
    IfElse = 91

    For = 100
    While = 101
    Loop = 102

    Suspend = 200
    Resume = 201
    Replace = 202

class Splice:
    def __init__(self, string, start, stop):
        self.string = string
        self.start = start
        self.stop = stop
    
    def text(self):
        return self.string[self.start:self.stop]
    
    def __str__(self):
        return self.text()
    
    def __len__(self):
        return self.stop - self.start

class Token:
    def __init__(self, ty, splice):
        self.type = ty
        self.splice = splice

class Executor:
    def __init__(self):
        self.stack = []
        self.variables = {}
    
    def pop(self):
        if len(self.stack) == 0:
            raise ValueError("Empty stack")
        return self.stack.pop()

    def process(self, tokens):
        for token in tokens:
            match token.type:
                case TokenType.Number:
                    self.stack.append(float(token.splice.text()))
                case TokenType.Plus:
                    self.process_binary_op(lambda a, b: a + b)
                case TokenType.Minus:
                    self.process_binary_op(lambda a, b: a - b)
                case TokenType.Dup:
                    if self.stack:
                        self.stack.append(self.stack[-1])
                case TokenType.QuotedIdent:
                    # Push the symbol name onto stack
                    self.stack.append(token.splice.text())
                case TokenType.Ident:
                    name = token.splice.text()
                    if name in self.variables:
                        self.stack.append(self.variables[name])
                    else:
                        raise ValueError(f"Undefined variable: {name}")
                case TokenType.Store:
                    if len(self.stack) < 2:
                        raise ValueError("Store needs 2 values: value and name")
                    name = self.pop()   # Variable name (top of stack)
                    value = self.pop()  # Value to store
                    self.variables[name] = value
                case TokenType.Assert:
                    result = self.pop()
                    if not result:
                        raise ValueError("Assert failed.")
    
    def print_data_stack(self):
        n = len(self.stack) - 1
        for element in self.stack:
            print(f"[{n}]: {element}")
            n = n - 1
    
    def process_binary_op(self, op):
        if len(self.stack) < 2:
            raise ValueError("Insufficient operands")
        b = self.pop()
        a = self.pop()
        self.stack.append(op(a, b))

def tokenize(input_str):
    """Convert input string into list of tokens"""
    tokens = []
    parts = input_str.split()
    pos = 0
    
    for part in parts:
        start = input_str.find(part, pos)
        end = start + len(part)
        pos = end
        
        # Determine token type
        if part.startswith('\''):
            token_type = TokenType.QuotedIdent
            start = start + 1  # Skip the quote in the splice
        elif part == '+':
            token_type = TokenType.Plus
        elif part == '-':
            token_type = TokenType.Minus
        elif part == '=':
            token_type = TokenType.Store
        elif part == 'dup':
            token_type = TokenType.Dup
        elif part == 'assert':
            token_type = TokenType.Assert
        elif part.isalpha():
            token_type = TokenType.Ident
        else:
            try:
                float(part)
                token_type = TokenType.Number
            except ValueError:
                print(f"Unknown token: {part}")
                continue
        
        splice = Splice(input_str, start, end)
        tokens.append(Token(token_type, splice))
    
    return tokens

def main():
    calc = Executor()
    while True:
        try:
            line = input("\nλ ").strip()
            
            if line.lower() in ('quit', 'exit', 'q'):
                break
            
            if line.lower() == 'clear':
                calc.stack.clear()
                print("Stack cleared")
                continue
            
            if not line:
                calc.print_data_stack()
                continue
            
            tokens = tokenize(line)
            calc.process(tokens)
            calc.print_data_stack()
            
        except ValueError as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nExiting...")
            break

if __name__ == "__main__":
    main()


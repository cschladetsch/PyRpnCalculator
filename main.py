# vi: set expandtab tabstop=4 shiftwidth=4 softtabstop=4:

from enum import Enum

class TokenType(Enum):
    Number = 1
    Plus = 2
    Minus = 3
    Dup = 4
    QuotedIdent = 5
    Ident = 6
    Store = 7
    Assert = 10

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
                    name = self.stack.pop()   # Variable name (top of stack)
                    value = self.stack.pop()  # Value to store
                    self.variables[name] = value
    
    def print_data_stack(self):
        n = len(self.stack) - 1
        for element in self.stack:
            print(f"[{n}]: {element}")
            n = n - 1
    
    def process_binary_op(self, op):
        if len(self.stack) < 2:
            raise ValueError("Insufficient operands")
        b = self.stack.pop()
        a = self.stack.pop()
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
        elif part.isalpha():
            token_type = TokenType.Ident
        elif part == '+':
            token_type = TokenType.Plus
        elif part == '-':
            token_type = TokenType.Minus
        elif part == '=':
            token_type = TokenType.Store
        elif part == 'dup':
            token_type = TokenType.Dup
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


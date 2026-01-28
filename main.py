from enum import Enum

class TokenType(Enum):
    Number = 1
    Plus = 2
    Minus = 3
    Dup = 4
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

class RpnCalc:
    def __init__(self):
        self.stack = []
    
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
    
    def print_data_stack(self):
        if not self.stack:
            print("Stack empty")
        elif len(self.stack) == 1:
            print(self.stack[0])
        else:
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
        if part == '+':
            token_type = TokenType.Plus
        elif part == '-':
            token_type = TokenType.Minus
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
    calc = RpnCalc()
    
    while True:
        try:
            line = input("\n> ").strip()
            
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

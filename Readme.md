# PyRpnCalc

A Reverse Polish Notation (RPN) calculator implemented in Python.

## Overview

PyRpnCalc is a stack-based calculator using postfix notation. Numbers are pushed onto a stack, and operators consume values from the stack to produce results.

## Features

- Persistent stack across multiple inputs
- Token-based lexer with source position tracking
- Type-safe operations using Python enums
- Interactive REPL interface

## Usage
```bash
python3 main.py
```

### Example Session
```
> 1 2 +
[0] 3.0

> 5 3 -
[1]: 2.0
[0]: 3.0

> *
6.0

> dup
[1]: 6.0
[0]: 6.0

> +
12.0

> clear

> quit
```

## Supported Operations

- `+` - Addition
- `-` - Subtraction
- `dup` - Duplicate top stack element
- `clear` - Clear the stack
- `quit`, `exit`, `q` - Exit calculator

## Architecture

- **Token**: Pairs a `TokenType` enum with a `Splice` for lexical analysis
- **Splice**: String view for efficient source position tracking (similar to `std::string_view`)
- **RpnCalc**: Stack-based calculator engine
- **tokenize()**: Lexer that converts input strings into token streams

## Requirements

- Python 3.10+ (uses pattern matching with `match`/`case`)


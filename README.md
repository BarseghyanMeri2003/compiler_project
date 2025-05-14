# Forthx86Compiler - A Forth-like Language Compiler for x86

## Features

- **Basic Arithmetic Operations**: `+`, `-`, `*`, `mod`, `neg`
- **Stack Manipulation**: `dup`, `drop`, `swap`, `over`, `nip`, `tuck`
- **I/O Operations**: `.` (print top of stack), `.s` (print stack contents)
- **Variables**: `variable` declaration, `!` (store), `@` (fetch)
- **Error Handling**: Stack underflow detection
- **Clean Output**: Properly formatted stack display

## Requirements

- Python 3.x
- NASM (Netwide Assembler)
- GCC (GNU Compiler Collection)
- x86 or x86-64 system (32-bit mode required)

## Installation

1. Clone or download this repository
2. Make the compiler executable:
   ```bash
   chmod +x forth_compiler.py
   ```

## Usage

### Compiling a Forth Program

```bash
./forth_compiler.py input.fs output.asm
```

### Assembling and Running

```bash
nasm -felf32 output.asm -o forth.o
gcc -m32 forth.o -o forth
./forth
```

## Language Syntax

### Numbers
Push integers onto the stack:
```
5 3 + .  \ Prints 8
```

### Arithmetic Operations
```
10 5 - .  \ Prints 5
7 3 * .   \ Prints 21
5 neg .   \ Prints -5
10 3 mod . \ Prints 1
```

### Stack Operations
```
1 dup .s    \ Duplicates top item
1 2 swap .s \ Swaps top two items
1 2 over .s \ Copies second item to top
1 2 nip .s  \ Removes second item
1 2 drop .s \ Drops top item
1 2 tuck .s \ Copies top item under second
```

### Variables
```
variable a
variable b
5 a !
3 b !
a @ .  \ Prints 5
b @ .  \ Prints 3
```

## Example Programs

See the `test.fs` file included in the repository for a comprehensive example demonstrating all features.

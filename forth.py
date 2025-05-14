#!/usr/bin/env python3
import sys
import re

class Forthx86Compiler:
    def __init__(self):
        self.words = {
            '+': self.compile_add,
            '-': self.compile_sub,
            '*': self.compile_mul,
            'dup': self.compile_dup,
            'swap': self.compile_swap,
            'tuck': self.compile_tuck,
            'neg': self.compile_neg,
            'drop': self.compile_drop,
            'over': self.compile_over,
            'mod': self.compile_mod,
            'nip': self.compile_nip,
            '.': self.compile_dot,
            '.s': self.compile_dot_s,
            '!': self.compile_store,
            '@': self.compile_fetch,
            'variable': self.handle_variable
        }
        self.variables = {}
        self.label_counter = 0
        self.output = []
        self.data_section = [
            "section .data",
            "int_format db '%d ',0", 
            "stack_start db 'Stack: ',0",
            "stack_end db '',10,0", 
            "empty_stack db '<empty>',10,0"
        ]
        self.bss_section = [
            "section .bss",
            "initial_esp resd 1"
        ]
        
    def compile(self, input_file, output_file):
        with open(input_file, 'r') as f:
            source = f.read()
        
        source = self.preprocess(source)
        tokens = source.split()
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token in self.words:
                if token == 'variable':
                    if i + 1 >= len(tokens):
                        raise ValueError("Missing variable name after 'variable'")
                    var_name = tokens[i+1]
                    self.compile_variable(var_name)
                    i += 2
                else:
                    self.words[token]()
                    i += 1
            elif token.isdigit():
                self.compile_literal(int(token))
                i += 1
            elif token in self.variables:
                self.compile_variable_ref(token)
                i += 1
            else:
                raise ValueError(f"Unknown word or invalid number: {token}")
        
        asm = self.generate_asm()
        with open(output_file, 'w') as f:
            f.write(asm)
        print(f"Successfully compiled {input_file} to {output_file}")

    def preprocess(self, source):
        source = re.sub(r'\\[^\n]*', '', source)  # Remove comments
        return ' '.join(source.split())  

    def new_label(self, prefix):
        self.label_counter += 1
        return f"{prefix}_{self.label_counter}"

    def handle_variable(self):
        pass

    def compile_variable(self, name):
        if name in self.variables:
            raise ValueError(f"Variable '{name}' already exists")
        self.variables[name] = len(self.bss_section)
        self.bss_section.append(f"{name}: resd 1")

    def compile_literal(self, n):
        self.output.append(f"    push {n}")

    def compile_dup(self):
        self.output.append("    mov eax, [esp]")
        self.output.append("    push eax")

    def compile_drop(self):
        self.output.append("    add esp, 4")

    def compile_swap(self):
        self.output.extend([
            "    pop eax",
            "    pop ebx",
            "    push eax",
            "    push ebx"
        ])

    def compile_add(self):
        self.output.extend([
            "    pop eax",
            "    add [esp], eax"
        ])

    def compile_sub(self):
        self.output.extend([
            "    pop ebx",
            "    pop eax",
            "    sub eax, ebx",
            "    push eax"
        ])

    def compile_mul(self):
        self.output.extend([
            "    pop eax",
            "    pop ebx",
            "    imul eax, ebx",
            "    push eax"
        ])

    def compile_tuck(self):
        self.compile_swap()
        self.compile_over()

    def compile_neg(self):
        self.output.append("    neg dword [esp]")

    def compile_over(self):
        self.output.extend([
            "    mov eax, [esp+4]",
            "    push eax"
        ])

    def compile_mod(self):
        self.output.extend([
            "    xor edx, edx",
            "    pop ebx",
            "    pop eax",
            "    idiv ebx",
            "    push edx"
        ])

    def compile_nip(self):
        self.compile_swap()
        self.compile_drop()

    def compile_dot(self):
        self.output.extend([
            "    push dword [esp]",
            "    push int_format",
            "    call printf",
            "    add esp, 8",
            "    push stack_end",
            "    call printf",
            "    add esp, 4",
            "    pop eax"
        ])

    def compile_dot_s(self):
        label = self.new_label("print_stack")
        end_label = self.new_label("end_stack")
        self.output.extend([
            "    push stack_start", 
            "    call printf",
            "    add esp, 4",
            
            "    mov ecx, esp",  
            f"{label}:",
            "    cmp ecx, [initial_esp]",  # Compare stack pointer with the starting point
            f"    jae {end_label}",  # If we're at the bottom of the stack, stop the loop
            "    push ecx",  # Save the current stack position
            "    push dword [ecx]",  # Push the current stack value to the printf argument list
            "    push int_format",   # Print format for an integer
            "    call printf",       # Call printf to print the value
            "    add esp, 8",        # Clean up the printf arguments
            "    pop ecx",           # Restore the stack position
            "    add ecx, 4",        # Move to the next stack element (4 bytes per element)
            f"    jmp {label}",      # Jump back to the loop start
        ])

        self.output.extend([
            f"{end_label}:",
            "    push stack_end",  # If the stack is empty, print a message
            "    call printf",
            "    add esp, 4",
        ])

    def compile_store(self):
        self.output.extend([
            "    pop ebx",  # address
            "    pop eax",  # value
            "    mov [ebx], eax"  # Store the value at the address (pointer)
        ])

    def compile_fetch(self):
        self.output.extend([
            "    pop eax",  # Get the address (pointer) from the stack
            "    mov eax, [eax]",  # Fetch the value from the address
            "    push eax"  # Push the fetched value back onto the stack
        ])

    def compile_variable_ref(self, name):
        self.output.append(f"    push {name}")

    def generate_asm(self):
        asm = [
            "global main",
            "extern printf",
            "section .text",
            "main:",
            "    mov [initial_esp], esp" 
        ]
        asm.extend(self.output)
        asm.extend([
            "    xor eax, eax",  
            "    ret"
        ])
        asm.extend(self.data_section)
        asm.extend(self.bss_section)
        return '\n'.join(asm)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <input.fs> <output.asm>")
        sys.exit(1)
    
    compiler = Forthx86Compiler()
    try:
        compiler.compile(sys.argv[1], sys.argv[2])
        print(f"Successfully compiled {sys.argv[1]} to {sys.argv[2]}")
        print("\nTo assemble and run:")
        print(f"nasm -felf32 {sys.argv[2]} -o forth.o")
        print("gcc -m32 forth.o -o forth")
        print("./forth")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

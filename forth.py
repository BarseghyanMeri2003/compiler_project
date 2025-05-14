class ForthInterpreter:
    def __init__(self):
        self.stack = []
        self.variables = {}

    def execute(self, commands):
        for line in commands.splitlines():
            line = line.split("\\")[0].strip()
            if not line:
                continue

            tokens = line.split()
            i = 0
            while i < len(tokens):
                token = tokens[i]

                if token == 'variable':
                    i += 1
                    if i >= len(tokens):
                        print("Error: variable name missing after 'variable'")
                        break
                    var_name = tokens[i]
                    self.push(var_name)
                    self.variable()

                elif token == 'store' or token == '!':
                    self.store()

                elif token == 'fetch' or token == '@':
                    self.fetch()

                elif token == '+':
                    self.add()

                elif token == '-':
                    self.subtract()

                elif token == '*':
                    self.multiply()

                elif token == 'dup':
                    self.dup()

                elif token == 'swap':
                    self.swap()

                elif token == 'drop':
                    self.drop()

                elif token == 'over':
                    self.over()

                elif token == 'mod':
                    self.mod()

                elif token == 'neg':
                    self.neg()

                elif token == 'nip':
                    self.nip()

                elif token == 'tuck':
                    self.tuck()

                elif token == '.':
                    self.print_top()

                elif token == '.s':
                    self.print_stack()

                elif token.isdigit() or (token.startswith('-') and
token[1:].isdigit()):
                    self.push(int(token))

                else:
                    self.push(token)

                i += 1

    def add(self):
        if len(self.stack) < 2:
            return
        b = self.stack.pop()
        a = self.stack.pop()
        self.push(a + b)

    def subtract(self):
        if len(self.stack) < 2:
            return
        b = self.stack.pop()
        a = self.stack.pop()
        self.push(a - b)

    def multiply(self):
        if len(self.stack) < 2:
            return
        b = self.stack.pop()
        a = self.stack.pop()
        self.push(a * b)

    def mod(self):
        if len(self.stack) < 2:
            return
        b = self.stack.pop()
        a = self.stack.pop()
        if b == 0:
            self.push(0)
        else:
            self.push(a % b)

    def dup(self):
        if self.stack:
            self.stack.append(self.stack[-1])

    def swap(self):
        if len(self.stack) < 2:
            return
        a = self.stack.pop()
        b = self.stack.pop()
        self.push(a)
        self.push(b)

    def drop(self):
        if self.stack:
            self.stack.pop()

    def over(self):
        if len(self.stack) < 2:
            return
        self.push(self.stack[-2])

    def neg(self):
        if self.stack:
            a = self.stack.pop()
            self.push(-a)

    def nip(self):
        if len(self.stack) < 2:
            return
        self.stack.pop(-2)

    def tuck(self):
        if len(self.stack) < 2:
            return
        top = self.stack.pop()
        second = self.stack.pop()
        self.push(top)
        self.push(second)
        self.push(top)

    def push(self, value):
        self.stack.append(value)

    def print_top(self):
        if self.stack:
            value = self.stack.pop()
            print(value)

    def print_stack(self):
        print(self.stack)

    def variable(self):
        if not self.stack:
            return
        var_name = self.stack.pop()
        if not isinstance(var_name, str):
            print(f"Invalid variable name: {var_name}. Variable names must be strings.")
            return
        if var_name not in self.variables:
            self.variables[var_name] = 0
        else:
            print(f"Variable {var_name} already exists.")

    def store(self):
        if len(self.stack) < 2:
            print("Error: Not enough items on stack for store (!) command.")
            return
        var_name = self.stack.pop()
        value = self.stack.pop()
        if not isinstance(var_name, str):
            print(f"Invalid variable name: {var_name}. Variable names must be strings.")
            return
        if var_name in self.variables:
            self.variables[var_name] = value
        else:
            print(f"Unknown variable: {var_name}. Please declare the variable first.")

    def fetch(self):
        if not self.stack:
            return
        var_name = self.stack.pop()
        if not isinstance(var_name, str):
            print(f"Invalid variable name: {var_name}. Variable names must be strings.")
            return
        if var_name in self.variables:
            self.push(self.variables[var_name])
        else:
            print(f"Unknown variable: {var_name}. Make sure the variable is declared first.")


def main():
    with open('test.fs', 'r') as file:
        forth_code = file.read()

    interpreter = ForthInterpreter()
    interpreter.execute(forth_code)


if __name__ == '__main__':
    main()

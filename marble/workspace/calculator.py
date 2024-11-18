import sys

# Define the calculator class

class Calculator:

    def __init__(self):
        pass

    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            raise ValueError('Cannot divide by zero')
        return a / b

# Define the command-line interface

def main():
    calculator = Calculator()
    while True:
        try:
            operation = input('Enter operation (add, subtract, multiply, divide, quit): ')
            if operation == 'quit':
                break
            a = float(input('Enter first number: '))
            b = float(input('Enter second number: '))
            if operation == 'add':
                result = calculator.add(a, b)
            elif operation == 'subtract':
                result = calculator.subtract(a, b)
            elif operation == 'multiply':
                result = calculator.multiply(a, b)
            elif operation == 'divide':
                result = calculator.divide(a, b)
            else:
                raise ValueError('Invalid operation')
            print('Result: ', result)
        except Exception as e:
            print('Error: ', str(e))

if __name__ == '__main__':
    main()
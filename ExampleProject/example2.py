# example2.py

def multiply(a, b):
    return a * b

def exponent(a, b):
    a ** b

def byProduct(a, b):
    return a * b

def divide(a, b):
    if b != 0:
        return a / b
    else:
        print("Cannot divide by zero")
        return None

def main():
    product = multiply(4, 5)
    print(f"Product: {product}")

    quotient = divide(10, 2)
    print(f"Quotient: {quotient}")

if __name__ == "__main__":
    main()

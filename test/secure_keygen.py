from string import digits ,punctuation ,ascii_letters
import random

def gen(number:int=20):
    symbols = ascii_letters+digits+punctuation
    secure_random = random.SystemRandom()
    password = "".join(secure_random.choice(symbols) for i in range(number))
    return str(password)
    
def gencode(number:int=6):
    symbols = ascii_letters+digits
    secure_random = random.SystemRandom()
    code = "".join(secure_random.choice(symbols) for i in range(number))
    return str(code).upper()
    
def gendigit(number:int=6):
    symbols = digits
    secure_random = random.SystemRandom()
    code = "".join(secure_random.choice(symbols) for i in range(number))
    return str(code).upper()
    
if __name__ == '__main__':
    print(gencode(6))
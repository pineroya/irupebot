import random

def roll_d6():
    return random.randint(1, 6)

def get_d6_img(n: int) -> str:
    return f'https://bormolina.github.io/assets/d6_{n}_sd.gif'
import random

def roll_d6():
    return random.randint(1, 6)

def get_d6_img(n: int) -> str:
    return f'https://bormolina.github.io/assets/d6_{n}_sd.gif'

def get_chard() -> str:
    chard = ['https://raw.githubusercontent.com/pineroya/dd/master/c-1.webp?token=GHSAT0AAAAAABWRD23YGNWBY36D74TWM3T2YXKRQQQ',
            'https://raw.githubusercontent.com/pineroya/dd/master/c-2.webp?token=GHSAT0AAAAAABWRD23YMS4SEHMMO7C7HLHEYXKSUEA',
            'https://raw.githubusercontent.com/pineroya/dd/master/c-3.webp?token=GHSAT0AAAAAABWRD23Z2R6LH7FGYXWAZDCWYXKSUYQ',
            'https://raw.githubusercontent.com/pineroya/dd/master/c-4.webp?token=GHSAT0AAAAAABWRD23YOFEGWKW2RBIQPTQAYXKSVMA',
            'https://raw.githubusercontent.com/pineroya/dd/master/c-5.webp?token=GHSAT0AAAAAABWRD23YUE4TIEZEF5QROFQ4YXKSV2A',
            'https://raw.githubusercontent.com/pineroya/dd/master/c-6.webp?token=GHSAT0AAAAAABWRD23YXACID4HI3HJOOOMEYXKSWMA',
            'https://raw.githubusercontent.com/pineroya/dd/master/c-7.webp?token=GHSAT0AAAAAABWRD23YBU776E7G7L56DCUKYXKSW4Q',
            'https://raw.githubusercontent.com/pineroya/dd/master/c-8.webp?token=GHSAT0AAAAAABWRD23ZFD26KSNICDAKMVQ2YXKSXFQ'
    ]
    return random.choice(chard)
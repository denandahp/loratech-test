import random

def generate_code_number(length: int) -> str:
    return ''.join(random.choice('0123456789')
                   for _ in range(length))


def generate_code(length: int) -> str:
    return ''.join(random.choice('ABCDEFGHIJKLMNOPRSTUVWXYZ0123456789')
                   for _ in range(length))
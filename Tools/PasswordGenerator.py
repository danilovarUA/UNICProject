import random
import string

LETTERS = string.ascii_letters
NUMBERS = string.digits
PUNCTUATION = string.punctuation
MAX_PASS_LENGTH = 20
MIN_PASS_LENGTH = 6


def generate_password():
    # characters = list(LETTERS + NUMBERS + PUNCTUATION)  # simplify password for debug purposes
    characters = list(LETTERS + NUMBERS)
    random.shuffle(characters)
    password = random.choices(characters, k=random.randint(MIN_PASS_LENGTH, MAX_PASS_LENGTH))
    password = ''.join(password)
    return password

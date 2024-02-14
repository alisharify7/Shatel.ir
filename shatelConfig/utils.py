import random
import secrets
from string import punctuation, digits, ascii_letters


def generate_secret_key(len_prob:int=6) -> str:
    """
    this function generates secure app_secret key for Flask app
    """
    token = [each for each in secrets.token_hex(80*len_prob)]
    token += random.choices(punctuation, k=80)
    token += random.choices(digits, k=80)
    token += random.choices(ascii_letters, k=80)
    random.shuffle(token)
    return "".join(token)

import random
import string

def generate_random_path(length, ext):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length)) + f'.{ext}'
    return result_str
from datetime import datetime
import random
import secrets
import string


def get_current_timestamp() -> str:
    """Returns the current timestamp in YYYY-MM-DD_HH-MM-SS format."""
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S") 

def roll_dice(sides: int = 6) -> int:
    """Simulates rolling a dice with the given number of sides."""
    return random.randint(1, sides)

def generate_password(length=12):
    character=(string.ascii_letters+string.digits+string.punctuation)

    password="" 
    for i in range(length):
        password+=secrets.choice(character)
    return password


def read_text_file(filename):
    content=None
    try:
        with open(filename,"r") as file:
            content=file.read()
        return content
    except FileNotFoundError:
        return f"Failed to read file {filename}"



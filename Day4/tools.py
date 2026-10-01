from datetime import datetime
import random


def get_current_timestamp() -> str:
    """Returns the current timestamp in YYYY-MM-DD_HH-MM-SS format."""
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S") 

def roll_dice(sides: int = 6) -> int:
    """Simulates rolling a dice with the given number of sides."""
    import random
    return random.randint(1, sides)
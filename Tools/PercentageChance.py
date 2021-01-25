import random
from deprecated import deprecated


@deprecated(reason="Use sampling instead")
def percentage_chance(percentage=20):
    value = random.randint(0, 100)
    if value <= percentage:
        return True
    else:
        return False

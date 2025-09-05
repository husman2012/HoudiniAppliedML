import random
import string

class RandomUtils:
    """
    Class for generation of random numbers
    """

    @staticmethod
    def generate_random_id() -> str:
        """
        Generates a radnom ID number as string of length 6
        """
        return "".join(random.choices(string.ascii_uppercase, k=6))
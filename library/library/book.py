from dataclasses import dataclass, field
from library.random_number_utils import RandomUtils

@dataclass(frozen=True, order=True, slots=True)
class Book:
    title: str
    genre: str
    author: str
    _price: float = 0.0
    id: str = field(default_factory = RandomUtils.generate_random_id)

    @property
    def price(self):
        """
        Gets price of Item, rounded to 2 decimal places
        """
        
        return round(self._price, 2)
    
    @property
    def search_string(self):
        """
        Gets the title, genre, and author of this object
        """
        return f"{self.title} {self.genre} {self.author}"
    
    @property
    def title(self):
        return self.title
    
    @property
    def genre(self):
        return self.genre

    @property
    def author(self):
        return self.author
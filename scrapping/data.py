from pydantic import BaseModel

class ScrappedReview(BaseModel):
    """
    Class to represent a TrustPilot review
    
    Attributes:
    ----------
    userName: str
        The name of the user who wrote the review
    reviewTitle: str
    rating: int
    comment: str
    date: str
    source: str
    company: int
        The id of the company (if the review concerns a company in general)
    restaurant: int
        The id of the restaurant (if the review concerns a restaurant)
    """

    userName: str
    reviewTitle: str
    rating: int
    comment: str
    date: str
    source: str
    company: int = None
    restaurant : int = None

class EcoReview(BaseModel):
    """
    Class to represent an EcoReview
    
    Attributes:
    ----------
    userName: str
        The name of the user who wrote the review
    category: str
        The category of the review ("organic", "climate", "waste", "social", "governance", "water", "greenwashing")
    rating: int
    comment: str
    date: str
    source: str
    company: int
        The id of the company (if the review concerns a company in general)
    restaurant: int 
        The id of the restaurant (if the review concerns a restaurant)
    """
    userName: str
    category: str = None
    rating: int = None
    comment: str
    date: str
    source: str
    company : int = None
    restaurant : int = None

class Company(BaseModel):
    """
    Class to represent a company

    Attributes:
    ----------
    name: str
        The name of the company
    id : int
        The id of the company
    name : str
    ecoScore : int
        the ecoScore of the company (sum of the ratings of the different categories)
    ratings : str
        the ratings of the company in the different categories in this order
            "environment (climate, waste, water), health (organic), governance (social, governance, greenwashing)"
    reviewCount : int
    """
    name: str
    id : int
    ecoScore : int = None
    ratings : str = None
    reviewCount : int = 0

class Restaurant(BaseModel):
    """
    Class to represent a restaurant

    Attributes:
    ----------
    id: int
        The id of the restaurant
    name: str
    company: int
        The id of the company
    address: str
    longitude: float
    latitude: float
    ecoScore: int
        the ecoScore of the restaurant (sum of the ratings of the different categories)
    ratings: str
        the ratings of the restaurant in the different categories in this order
            "environment (climate, waste, water), health (organic), governance (social, governance, greenwashing)"
    reviewCount: int
    """
    id: int
    name: str
    company: int
    address: str
    longitude: float
    latitude: float
    ecoScore: int = None
    ratings: str = None
    reviewCount: int = 0

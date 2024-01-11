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
    restaurantName: str
    """

    userName: str
    reviewTitle: str
    rating: int
    comment: str
    date: str
    source: str
    restaurantName: str

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
    restaurantName: str
    """
    userName: str
    category: str = None
    rating: int = None
    comment: str
    date: str
    source: str
    restaurantName: str


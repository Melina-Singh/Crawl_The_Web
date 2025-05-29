from pydantic import BaseModel
from typing import List

class Project(BaseModel):
    """
    Represents the data structure of a Venue.
    """

    name: str
    location: str
    sector: str
    area: str
    focus: List[str]
    partners: List[str]
    heritage: List[str]
    vegetation: str
    accessibility: str
    history: str
    description: str
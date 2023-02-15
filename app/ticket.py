from pydantic import BaseModel
from typing import Optional

class Ticket(BaseModel):
    ticket_id: str
    name: str
    from_city: str
    to_city: str
    gate: int
    price: float
    date: str
    file: Optional[bytes] = None 
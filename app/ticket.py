from pydantic import BaseModel

class Ticket(BaseModel):
    ticket_id: str
    name: str
    from_city: str
    to_city: str
    gate: int
    price: float
    date: str
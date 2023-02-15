from pydantic import BaseModel, Optional

class Ticket(BaseModel):
    ticket_id: str
    name: str
    from_city: str
    to_city: str
    gate: int
    price: float
    date: str
    file: bytes | None = None
from fastapi import FastAPI, Response, Request, File, HTTPException
from typing import Optional 
from redis_functions import RedisInterface
import ticket
import uuid



app = FastAPI()
redisThings = RedisInterface()

"""
Description:
    Root url. To indicate that all is well.
Parameters:
    None
Returns:
    String
"""
@app.get("/")
def read_root(request: Request):
    return "Host is up and running"





"""
Description:
    Helps create ticket with along with ticket id
Parameters:

Returns:

"""
@app.post("/create_ticket")
async def create_ticket(ticket: ticket.Ticket):
    if not ticket.date or not ticket.name or not ticket.from_city or not ticket.price or not ticket.to_city or not ticket.gate:
        raise HTTPException(status_code=400, detail="Bro something is wrong (hint: there's null values somewhere in your request). Fix it") 
    ticket.ticket_id = str(uuid.uuid4())
    redisThings.insert(ticket)

    if not redisThings.get_by_key(ticket.ticket_id):
        return "Failed to create for some reasons"

    return ticket





"""
Description:
    This method is created seperately because, we can use the pipeline function to batch insert
    multiple values, instead of calling the redisThings.insert function multiple times. 
Parameters:


Returns:
    Custom HTTP response if number of fields are incorrect
"""
@app.post("/create_many_tickets")
async def create_many_tickets(ticketList: list, response: Response):

    fields = {
        "ticket_id",
        "name",
        "from_city",
        "to_city",
        "gate",
        "price",
        "date",
        "file"
    }
    """
        Finding union is much faster below, as otherwise, we have to perform nested loops with
        O(keys*number_of_entries) complexity. 
    """
    for ticket in ticketList:
        union = fields.union(ticket.keys())
        # this is a check to see if the fields are consistent
        if len(union) > 8:
            raise HTTPException(status_code=404, detail="Incorrect number of fields bRo")
        ticket['ticket_id'] = str(uuid.uuid4())
    redisThings.insert_many(ticketList)
    return ticketList






"""
Description:
    This method uploads a file to the key mentioned in the path. This is seperated from the 
    insert function because insert() inserts a ticket object, that is converted to a dict 
    before uploading

    upload file receives a dict object and directly uploads it by appending the file object 
    to it as a string

Parameters:
    ticket_id, from the path
    fileName, which is a bytes object from the body of the request

Returns:

"""
@app.put("/upload_file/{ticket_id}")
async def upload_file(ticket_id: str, fileName: bytes = File()):
    keys = redisThings.r.keys()
    if ticket_id not in keys:
        raise HTTPException(status_code=400, detail="Key does not exist")
    ticket = redisThings.get_by_key(ticket_id)

    if ticket:
        ticket = {
            "ticket_id": ticket["ticket_id"],
            "name": ticket["name"],
            "from_city" : ticket["from_city"],
            "to_city" : ticket["to_city"],
            "gate" : ticket["gate"],
            "price" : ticket["price"],
            "date": ticket["date"],
            "file": fileName.decode('ascii')
        }
        redisThings.upload_file(ticket)
        if redisThings.get_by_key(ticket["ticket_id"]): 
            return "created successfully"
        else:
            raise HTTPException(status_code=400, detail="Upload file error")
    else:
        raise HTTPException(status_code=400, detail="ID not found")





"""
Description:
    This method is created seperately because, we can use the pipeline function to batch insert
    multiple values, instead of calling the redisThings.insert function multiple times. 
Parameters:

Returns:

"""
@app.delete("/delete_ticket_by_id/{ticket_id}")
def delete_ticket_by_id(ticket_id: str):
    redisThings.delete_by_key(ticket_id)
    return "Key was deleted successfully"





"""
Description:
    This method is created seperately because, we can use the pipeline function to batch insert
    multiple values, instead of calling the redisThings.insert function multiple times. 
Parameters:

Returns:

"""
@app.delete("/delete_all")
def delete_all_tickets():
    redisThings.delete_all()
    if redisThings.get_all():
        return "Keys were not deleted successfully"
    return "Keys were all deleted successfully"






"""
Description:
    This method helps retrieve all the tickets in the  redis database.
Parameters:

Returns:

"""
@app.get("/get_all_tickets")
def get_all_tickets(
    request: Request,
    response: Response,
    sortBy: Optional[str] = None, 
    limit: Optional[int] = None,
    offset: Optional[int] = None
    ):
  
    data = redisThings.get_all()
    if sortBy:
        data = sorted(data, key=lambda d: d[sortBy])

    if limit:
        if offset:
            data = data[0 if (offset<0 or offset>len(data)) else offset :]
        data = data[: len(data) if (limit > len(data) or limit < 0) else limit]

        return data if data else "data is empty"

    if offset:
        data = data[0 if offset<0 else offset :]
   
        
    return data if data else "data is empty"
    





"""
Description:
    This method assumes you know the ticket id, and retreives the ticket based on the id 
Parameters:
    From

Returns:

"""
@app.get("/get_ticket_by_id/{ticket_id}")
def get_ticket_by_id(ticket_id: Optional[str] = None):
    if not ticket_id:
        data = redisThings.get_all()

    data = redisThings.get_by_key(ticket_id)
    if data:
        return data
    else:
        raise HTTPException(status_code=200, detail="Data is empty bRo")





"""

END OF FILE

"""
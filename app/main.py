from fastapi import FastAPI, Response, Request, File, UploadFile
from typing import Optional 
import redis
from redis_functions import RedisInterface
import ticket
import uuid

"""
Sample request body:
{ 
    "ticket_id":"f82b4dkc",
    "name": "Fauzaan",
    "from_city" : "Singapore",
    "to_city" : "Berkley",
    "gate" : 48,
    "price" : 876.12,
    "date": "5th June 2024"
}
Sample request body to insert many:
[
    { 
        "ticket_id":"f82b4dkc",
        "name": "Ted",
        "from_city" : "Prague",
        "to_city" : "Washington",
        "gate" : 12,
        "price" : 1000,
        "date": "5th June 2024"
    },
    { 
        "ticket_id":"f82b4dkc",
        "name": "Lily",
        "from_city" : "England",
        "to_city" : "Washington",
        "gate" : 48,
        "price" : 1020,
        "date": "10th June 2024"
    },
    { 
        "ticket_id":"f82b4dkc",
        "name": "Boldimir",
        "from_city" : "Iceland",
        "to_city" : "Helsinki",
        "gate" : 11,
        "price" : 80,
        "date": "9th June 2024"
    }
]

"""

app = FastAPI()
redisThings = RedisInterface()

"""
Description:
    Root url. To indicate that all is well.
Parameters:

Returns:

"""
@app.get("/")
def read_root(request: Request):
    return "Host is up and running"





"""
Description:
    This method is created seperately because, we can use the pipeline function to batch insert
    multiple values, instead of calling the redisThings.insert function multiple times. 
Parameters:

Returns:

"""
@app.post("/create_ticket")
async def create_ticket(ticket: ticket.Ticket, response: Response):
    # print("ticket", ticket)
    if not ticket:
        response.status_code = 404
        return "Entity was not found"
    ticket.ticket_id = str(uuid.uuid4())
    redisThings.insert(ticket)
    """
    Code to check if it has indeed been created
    """

    return ticket





"""
Description:
    This method is created seperately because, we can use the pipeline function to batch insert
    multiple values, instead of calling the redisThings.insert function multiple times. 
Parameters:

Returns:

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
    "date"
    }
    """
        Finding union is much faster below, as otherwise, we have to perform nested loops with
        O(keys*number_of_entries) complexity. 
    """
    for ticket in ticketList:
        union = fields.union(ticket.keys())
        # this is a check to see if the fields are consistent
        if len(union) > 7:
            response.status_code = 404
            return "Incorrect number of fields or field names!"
        ticket['ticket_id'] = str(uuid.uuid4())
    redisThings.insert_many(ticketList)
    return ticketList





"""
Description:
    This method uploads a file to the key mentioned in  
Parameters:

Returns:

"""
@app.post("/upload_file/{ticket_id}")
def upload_file(ticket_id: str, fileName: bytes = File()):
    data = redisThings.get_by_key(ticket_id)
    if data:
        # file_to_upload = fileName.read()
        data['file'] =  fileName
        redisThings.insert(data)
        return data



# there is change


"""
Description:
    This method is created seperately because, we can use the pipeline function to batch insert
    multiple values, instead of calling the redisThings.insert function multiple times. 
Parameters:

Returns:

"""
@app.delete("/delete_ticket_by_id/{ticket_id}")
def delete_ticket_by_id(ticket_id: str):
    """
    Code to delete a ticket by ticket id from redis db
    """
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
    """
    Code to delete a ticket by ticket id from redis db
    """
    redisThings.delete_all()
    return "Keys were all deleted successfully"






"""
Description:
    This method is created seperately because, we can use the pipeline function to batch insert
    multiple values, instead of calling the redisThings.insert function multiple times. 
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
    try:
        data = redisThings.get_all()
        if sortBy:
            data = sorted(data, key=lambda d: d[sortBy])

        if limit:
            if offset:
                data = data[0 if (offset<0 or offset>len(data)) else offset :]
            # print(data)
            data = data[: len(data) if (limit > len(data) or limit < 0) else limit]

            return data if data else "data is empty"

        if offset:
            data = data[0 if offset<0 else offset :]
    except: 
        print("There was an error")
    return data if data else "data is empty"
    





"""
Description:
    This method assumes you know the ticket id somehow 
Parameters:

Returns:

"""
@app.get("/get_ticket_by_id/{ticket_id}")
def get_ticket_by_id(ticket_id:str):
    data = redisThings.get_by_key(ticket_id)
    return data if data else "data is empty"





"""

END OF FILE

"""
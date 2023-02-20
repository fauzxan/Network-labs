import redis
import ticket
import json
from typing import Optional

"""
Function list:
    1. insert(ticket): to insert a single ticket
    2. insert_many(ticketList): uses batch insertion with the help of pipiline function
    3. get_all(): gets all the entries in the redis database
    4. get_by_key(key): gets the entry where the key is equal to the key provided as parameter
    5. delete(): deletes all the entries
    6. delete_by_key(): deletes a specific entry
"""

class RedisInterface:
    def __init__(self):
        self.r = redis.Redis(host="redis", db=0)
        if self.r.ping() == True:
            print("\n\n\nRedis service is running")
        else:
            print("\n\n\nRedis server error")

    # good
    def insert(self, ticket: ticket.Ticket):
        if self.r:
            val = {
                "ticket_id": ticket.ticket_id,
                "name": ticket.name,
                "from_city" : ticket.from_city,
                "to_city" : ticket.to_city,
                "gate" : ticket.gate,
                "price" : ticket.price,
                "date": ticket.date,
                "file": ticket.file.decode('ascii') if ticket.file else ""
            }
            self.r.set(ticket.ticket_id, json.dumps(val))
        else:
            print("\n\n\nUnable to insert the values! Redis instance was not instantiated properly")    
    
    def insert_many(self, ticketList: list):
        if self.r:
            pipe = self.r.pipeline() # this is the main difference between insert and insert many
            for ticket in ticketList:
                val = { 
                    "ticket_id": ticket["ticket_id"],
                    "name": ticket["name"],
                    "from_city" : ticket["from_city"],
                    "to_city" : ticket["to_city"],
                    "gate" : ticket["gate"],
                    "price" : ticket["price"],
                    "date": ticket["date"],
                    "file": ticket["file"].decode('ascii') if "file" in ticket else " "
                }
                self.r.set(ticket['ticket_id'], json.dumps(val))
            pipe.execute()
        else:
            print("\n\n\nUnable to insert the values, as there was a redis error!")        
    
    def upload_file(self, ticket: dict):
        if self.r:
            self.r.set(ticket["ticket_id"], json.dumps(ticket))
        else:
            print("\n\n\nUnable to insert the values! Redis instance was not instantiated properly")    
    

    def get_all(self):
        if self.r:
            keys = self.r.keys()
            data = []
            for key in keys:
                data.append(json.loads(self.r.get(key)))
            return data

    #good
    def get_by_key(self, key: str):
        if self.r:
            data = self.r.get(key)
            return json.loads(data) if data else None
        else:
            return "\n\n\nUnable to get the values, as there was a redis error!"


    def delete_all(self, originCity: Optional[str] = None):
        if self.r:
            keys = self.r.keys('*')
            if originCity:
                for key in keys:
                    data = json.loads(self.r.get(key))
                    print(data)
                    if data['from_city'] == originCity:
                        self.r.delete(key)
            else:
                self.r.delete(*keys)
            return True
        else:
            return False


    def delete_by_key(self, key: str):
        if self.r:
            self.r.delete(key)
            return True
        else:
            return False
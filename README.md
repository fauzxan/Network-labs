# Networks Lab 2 - REST API
The repository demonstrates the backend functionality of a ticketing system made using the following technology: <br/>

- FastAPI on python
- Redis Database
- Docker-compose

<br/>

## Setup
Open the code in your IDE. Open a terminal, and cd to project directory. Also make sure your docker daemon is running in the background. Once there run the following command:<br/>
```
docker-compose-up
```
## Methods used 
> The expected response for each code has been given in the code. In main.py, the Description, input and output of each function is documented for your reference.

#### GET methods
1. "/" default root directory: Just an indicator of if the host is up and running as expected.
2. "/get_all_tickets"
You can specify the following query parameters for this method: sortBy, limit, and offset
3. "/get_ticket_by_id/{ticket_id}": This method assumes you know the ticket_id of the individual. (This can be retrieved during creation, or via /get_all_tickets?sortBy=name) 
<br/>

#### POST methods
1. "/create_ticket": Creates one singular ticket, and automatically generates the ticket_id along with the hash for it.
2. "create_many_tickets": Takes in JSON string in the HTTP request and perfoms batch insert with pipelining.
<br/>

#### DELETE method
1. "/delete_all": Performs pattern matching and deletes all the keys in the directory
2. "delete_ticket_by_id": Deletes ticket based on the id passed into the url. This method also assumes you know the ticket_id to be deleted (This can be retrieved during creation, or via /get_all_tickets?sortBy=name).
<br/>

#### PUT method
1. "/upload_file/{ticket_id}": Takes in a multipart/form request as a .txt file and uploads the file (boarding pass) to the ticket_id specified. This method also assumes that you know the ticket_id (This can be retrieved during creation, or via /get_all_tickets?sortBy=name). For ease of testing, a sample_ticket.txt file has been provided in the project directory.
<br/>

#### 
> For all the methods, where query parameters or path parameters are present, you need to modify the request in the test file. You also need to modify the request for upload_file to your custom directory.

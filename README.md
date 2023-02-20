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
1. "/" default root directory<br/> Just an indicator of if the host is up and running as expected.
2. "/get_all_tickets"<br/>
You can specify the following query parameters for this method: sortBy, limit, and offset
3. "/get_ticket_by_id/{ticket_id}"<br/>This method assumes you know the ticket_id of the individual. (This can be retrieved during creation, or via /get_all_tickets?sortBy=name) 
<br/>

#### POST methods
1. "/create_ticket"<br/>Creates one singular ticket, and automatically generates the ticket_id along with the hash for it.
2. "create_many_tickets"<br/> Takes in JSON string in the HTTP request and perfoms batch insert with pipelining.
3. "/upload_file/{ticket_id}"<br/> Takes in a multipart/form request as a .txt file and uploads the file (boarding pass) to the ticket_id specified. This method also assumes that you know the ticket_id (This can be retrieved during creation, or via /get_all_tickets?sortBy=name). For ease of testing, a sample_ticket.txt file has been provided in the project directory.
<br/>

#### DELETE methods
1. "/delete_all"<br/> Performs pattern matching and deletes all the keys in the directory
2. "delete_ticket_by_id"<br/> Deletes ticket based on the id passed into the url. This method also assumes you know the ticket_id to be deleted (This can be retrieved during creation, or via /get_all_tickets?sortBy=name).
<br/>



#### 
> For all the methods, where query parameters or path parameters are present, you need to modify the request in the test file. You also need to modify the request for upload_file to your custom directory.

#### Features implemented (checkoff requirements)

1. GET request
- with no query parameters
- with a sortBy query parameter, to transform the order of the items returned
- with a limit query parameter, to limit the number of items returned
- with a offset query parameter, to "skip" ahead by a number of items
- with any combination of the above query parameters
<br/>

2. POST request
- that creates a new resource with the given attributes in the body
- show that the resource has indeed been created through another HTTP request. You can check that a ticket has been created either with a get_ticket_by_id or a get_all_tickets request
- has validation and returns an appropriate HTTP response code along with a '{error} bRo' message if the input data is invalid (e.g. missing name). 
<br/>

3. DELETE request
- that deletes or updates a single resource respectively
- show that the resource has indeed been modified through another HTTP request = has validation and returns an appropiate HTTP response code if the input data is invalid (e.g. trying to delete a nonexistent user). This also throws a '{error} bRo' message.
<br/>

4. Indempotent routes in my application: only the post upload_file path is indempotent as sending the same file to the same user will always result in the same result.<br/>

5. Challenges implemented from checkoff:
- File upload in a POST request, using multipart/form-data
- A special route that can performs batch delete based on a query parameter- originCity. This is done to resemble a scenario where all flights from a specific city are cancelled. 

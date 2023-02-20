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
#### GET methods
- "/" default root directory
- "/get_all_tickets"
You can specify the following query parameters for this method:
- sortBy

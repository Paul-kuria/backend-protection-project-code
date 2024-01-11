
**Frameworks**
Core Tech: Python

Backend Service: FastAPI, fastapi-mqtt library, MQTT

Database: postgreSQL

Documentation: Swagger



## Setup 

Open the project directory backend_protection_project, the docker-compose file should be present in this root path. Run the command below:

**Build Docker Containers**
```console 
docker-compose up -d --build
```

### Run the program locally

**Connect to API**
Enter this in your browser, and Connect to swagger documentation to begin testing the app.

```console
http://localhost:5000/docs
```

Each api has been well documented within swagger and expected inputs and outputs labelled as should be.
I decided to use a combination of real time data inputs with lists, as well as storing data inside a postgreSQL database, especially useful for fetching the list of device id's and latest status responses.

![Screenshot](backend.png)
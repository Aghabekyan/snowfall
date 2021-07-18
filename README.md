# Snowfall Issue tracker
## Getting Started
These instructions will get you a copy of the project up and running on your local machine. See deployment for notes on how to deploy the project.
### Prerequisites
What additional tools you need to install and build the app:
* Docker Engine
* Docker Compose
# Rest APIs
See documentation on http://127.0.0.1:8181/swagger-docs

## Deployment

Clone or download the project. Go to the backend directory and run the following commands to build and run the app
```
docker-compose pull
docker-compose build
docker-compose up
the application running on 127.0.0.1:8181
```
Application is ready to use.
## Simple Unit Tests

Run following command inside backend directory
```
make test
```

## Built With
* [Python 3+](https://docs.python.org/3/)
* [Django v3.1.2](https://www.djangoproject.com/)
* [PostgreeSQL](https://www.postgresql.org/)
* [Docker](https://www.docker.com/)


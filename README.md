# Eco-index API Stack

The Eco-index API stack repo includes the code for the backend FastAPI app and frontend REACT app for the Eco-index Database.  The stack is designed for Docker Compose deployment using either the docker-compose.yml file for development deployment and docker-compose.prod.yml file for production deployment.  Production deploys using the stable branch of the code.

## Features

- Backend FastAPI for user management and database queries utilising pydantic models and SQL Alchemy
- Frontend REACT app designed to connect with the backend API to create and manage user accounts, and create filtered queries
- Traefik network load balancing and direction via direct deployment on Docker Compose

The current [development version] and [stable version] are both available as Docker images on Docker Hub.

## Development Deployment

To contribute deploy via Docker using docker-compose.yaml after forking the project
```
docker-compose up
```
You will need to create a prodscripts directory in the project directory to hold the following files:
- *./prodscripts/env/.env* - to hold environment variables
- *./prodscripts/occurrence_download* - to hold generated download files of occurrence
- *./prodscripts/migrations* - to hold database migration files
- *./prodscripts/templates* - to hold email templates
- *./prodscripts/location_data* - to hold polygons for testing

Example database migration files can be found at [this repo]

## Docker Deployment

To deploy the project for production, download only the docker-compose.prod.yaml and frontend directory into the same directory
```
docker-compose up docker-compose.prod.yaml
```
You will need to create a prodscripts directory in the parent directory to hold the following files:
- *./prodscripts/env/.env* - to hold environment variables
- *./prodscripts/occurrence_download* - to hold generated download files of occurrence
- *./prodscripts/migrations* - to hold database migration files
- *./prodscripts/templates* - to hold email templates

## License

This project is licensed under GPL v3

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [development version]: <https://hub.docker.com/layers/190209917/ecoindex/ecoindex-backend/main/images/sha256-02a3d1da1eefbc3b13ca114c7ebf90f9310c01fc53f4157b11d32e047587507d?context=repo>
   [stable version]: <https://hub.docker.com/layers/201226662/ecoindex/ecoindex-backend/stable/images/sha256-130c3e768cd573004e87eef662f7de6dc4f49eb7d253aa1e612c34cf401efa15?context=repo>
   [this repo]: <https://github.com/eco-index/ecoindex-db-migrations>

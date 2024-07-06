# Docker Documentation for news_factory_server

This document provides instructions for building, running, and managing the Docker containers for the `news_factory_server` project.

## Directory Structure

The following files are located in the `deployments/` directory:

```
deployments/
├── Dockerfile
├── docker-compose.yml
└── .dockerignore
```

### Files Overview

- **Dockerfile**: Defines the Docker image for the project.
- **docker-compose.yml**: Example Docker Compose file that can be copied and modified to run the application on a local machine.
- **.dockerignore**: Specifies which files and directories should be ignored by Docker.

## Building and Running the Docker Container

### Prerequisites

Ensure you have Docker and Docker Compose installed on your machine.

### Using Docker Compose

#### Step-by-Step Guide

1. **Navigate to the Project Directory**

   Navigate to the root directory of your project:

   ```bash
   cd /path/to/your/project
   ```

2. **Copy the Example Docker Compose File**

   Copy the example `docker-compose.yml` file to `deployments/local_docker-compose.yml` for your local environment setup:

   ```bash
   cp deployments/docker-compose.yml deployments/local_docker-compose.yml
   ```

3. **Modify the `local_docker-compose.yml` File**

   Open `deployments/local_docker-compose.yml` and modify it to suit your local environment. Ensure the paths are correctly set for your local data and configuration files.

4. **Build the Docker Image**

   Use the `--build` flag with `docker-compose up` to rebuild the image:

   ```bash
   docker-compose -f deployments/local_docker-compose.yml up --build -d
   ```

#### Example Docker Compose File (`docker-compose.yml`)

This is an example Docker Compose file that you can copy and modify to run the application on your local machine.

```yaml
services:
  news_factory:
    container_name: news_factory_server
    build:
      context: ..
      dockerfile: ./deployments/Dockerfile
    ports:
      - "8036:8036"
    environment:
      FLASK_APP: run.py
      FLASK_RUN_HOST: 0.0.0.0
      CONFIG_PATH: /usr/src/app/config.json
    volumes:
      - ..:/usr/src/app
      - /path/to/your/project/data:/usr/src/app/data
      - ../config_docker.json:/usr/src/app/config.json
    command: ["python", "run.py", "--config", "/usr/src/app/config.json"]
```

> [!NOTE]
> `- /path/to/your/project/data:/usr/src/app/data` needs to be modified to point to your mapped data directory.

#### Custom Docker Compose File (`local_docker-compose.yml`)

This Docker Compose file is used to run the local server. It is customized for my local development environment.

```yaml
services:
  news_factory:
    container_name: news_factory_server
    build:
      context: ..
      dockerfile: ./deployments/Dockerfile
    ports:
      - "8036:8036"
    environment:
      FLASK_APP: run.py
      FLASK_RUN_HOST: 0.0.0.0
      CONFIG_PATH: /usr/src/app/config.json
    volumes:
      - ..:/usr/src/app
      - /Users/egodraconis/Library/Mobile Documents/com~apple~CloudDocs/rabbits_hole/calendars:/usr/src/app/data
      - ../config_docker.json:/usr/src/app/config.json
    command: ["python", "run.py", "--config", "/usr/src/app/config.json"]

```

I set a custom config JSON file to point to the docker mapped data directory:

```json
{
    "configurations": [
        {
            "name": "today",
            "description": "Today's event data",
            "end_point": "today.ics",
            "file": "/usr/src/app/data/calendar_data_today_cleaned_data.json"
        }
    ]
}
```

### Building and Using the Docker Image Directly

If you prefer to build and run the Docker container directly without using Docker Compose, follow these steps:

1. **Navigate to the Project Directory**

   Navigate to the root directory of your project:

   ```bash
   cd /path/to/your/project
   ```

2. **Build the Docker Image**

   Use the following command to build the Docker image:

   ```bash
   docker build -f ./deployments/Dockerfile -t news_factory_server .
   ```

3. **Remove Any Existing Container**

   If there's already a container running with the same name, remove it:

   ```bash
   docker rm -f news_factory_container
   ```

4. **Run the Docker Container**

   Use the following command to run the Docker container:

   ```bash
   docker run -d -p 8036:8036 --name news_factory_container -v /path/to/your/data:/usr/src/app/data -v /path/to/your/config_file.json:/usr/src/app/config.json news_factory_server
   ```

#### Example of a Customized Command Line

Here is an example command customized for specific local paths:

```bash
docker run -d -p 8036:8036 --name news_factory_container -v '/Users/egodraconis/Library/Mobile Documents/com~apple~CloudDocs/rabbits_hole/calendars':/usr/src/app/data -v '/Users/Jimmy/websharp/projects/python/forexfactory/news_factory_server/config_docker.json':/usr/src/app/config.json news_factory_server
```

## Common Docker Commands

### Building the Docker Image

To build the Docker image, use the following command:

```bash
docker-compose -f deployments/local_docker-compose.yml build
```

### Running the Docker Container

To run the Docker container, use the following command:

```bash
docker-compose -f deployments/local_docker-compose.yml up -d
```

### Stopping the Docker Container

To stop the Docker container, use the following command:

```bash
docker-compose -f deployments/local_docker-compose.yml down
```

### Viewing Logs

To view the logs of the running container, use the following command:

```bash
docker logs news_factory
```

### Inspecting the Container

To inspect the container and verify volume mounts, use the following command:

```bash
docker inspect news_factory
```

## Troubleshooting

### Container Fails to Start

If the container fails to start, check the logs for error messages:

```bash
docker logs news_factory
```

### File Not Found Errors

Ensure that the paths in the `docker-compose.yml` file are correct and that the files exist at those locations.

## Conclusion

This document provides the necessary steps to build, run, and manage Docker containers for the `news_factory_server` project. If you encounter any issues, refer to the troubleshooting section or check the Docker logs for more details.

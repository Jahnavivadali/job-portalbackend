# Job Portal Backend

A Flask-based backend application for a Job Portal system. The backend provides APIs for managing job-related operations and connects with the application database.

## Technologies Used

* Python
* Flask
* MySQL
* Docker
* REST APIs

## Project Structure

```text
job-portalbackend/
├── app.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
└── README.md
```

## Docker

Docker is used to package the Flask backend and its dependencies into a portable container. This makes it easier to build, run, and deploy the application consistently across different environments.

### Prerequisites

Before running the application with Docker, make sure Docker Desktop is installed and running.

Check the Docker installation:

```bash
docker --version
```

Check that Docker is running:

```bash
docker info
```

### Build Docker Image

Build the Docker image from the project directory:

```bash
docker build -t vadalijahnavi/job-portal-backend:latest .
```

A versioned image can also be created:

```bash
docker tag vadalijahnavi/job-portal-backend:latest vadalijahnavi/job-portal-backend:v1.0
```

### Run Docker Container

Run the backend container using port mapping:

```bash
docker run -d -p 5000:5000 --name job-portal-backend-container vadalijahnavi/job-portal-backend:latest
```

The `-p 5000:5000` option maps port `5000` of the host machine to port `5000` inside the Docker container.

### Check Running Container

To verify that the container is running:

```bash
docker ps
```

The container should show an `Up` status with the port mapping:

```text
0.0.0.0:5000->5000/tcp
```

### Test the Application

Test the backend using:

```bash
curl http://localhost:5000
```

Expected response:

```text
Backend running
```

The application can also be accessed through a web browser:

```text
http://localhost:5000
```

### View Container Logs

To view the application startup and runtime logs:

```bash
docker logs job-portal-backend-container
```

To continuously monitor the logs:

```bash
docker logs -f job-portal-backend-container
```

### Stop the Container

To stop the running container:

```bash
docker stop job-portal-backend-container
```

### Start the Container Again

```bash
docker start job-portal-backend-container
```

### Remove the Container

```bash
docker rm job-portal-backend-container
```

## Pull Image from Docker Hub

The Docker image is available on Docker Hub.

Pull the latest version:

```bash
docker pull vadalijahnavi/job-portal-backend:latest
```

Pull version `v1.0`:

```bash
docker pull vadalijahnavi/job-portal-backend:v1.0
```

## Run the Pulled Image

After pulling the image, run it using:

```bash
docker run -d -p 5000:5000 --name job-portal-backend-container vadalijahnavi/job-portal-backend:latest
```

## Docker Hub

Docker Hub repository:

`vadalijahnavi/job-portal-backend`

The repository contains both:

* `latest`
* `v1.0`

## Docker Workflow

The basic Docker workflow used for this project is:

```text
Dockerfile
    ↓
docker build
    ↓
Docker Image
    ↓
docker run
    ↓
Docker Container
    ↓
Application running on localhost:5000
```

## Conclusion

The Job Portal backend is containerized using Docker, allowing the application to be built and executed in an isolated and consistent environment. The Docker image can also be published to Docker Hub and pulled on another system for deployment.

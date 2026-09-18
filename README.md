# Job Portal Backend

A Flask-based backend application for a Job Portal system. It provides REST APIs and connects with a MySQL database.

## Technologies Used

* Python
* Flask
* MySQL
* Docker

## Project Structure

```text
job-portalbackend/
├── app.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
└── README.md

## Docker

Docker is used to containerize the Flask backend and its dependencies.

### Prerequisites

Make sure Docker Desktop is installed and running.

Check Docker:

```bash
docker --version
```

### Build Docker Image

```bash
docker build -t vadalijahnavi/job-portal-backend:latest .
```

Create a version tag:

```bash
docker tag vadalijahnavi/job-portal-backend:latest vadalijahnavi/job-portal-backend:v1.0
```

### Run Docker Container

```bash
docker run -d -p 5000:5000 --name job-portal-backend-container vadalijahnavi/job-portal-backend:latest
```

The application runs on:

```text
http://localhost:5000
```

### Check Container

```bash
docker ps
```

### Test Application

```bash
curl http://localhost:5000
```

Expected response:

```text
Backend running
```

### View Logs

```bash
docker logs job-portal-backend-container
```

### Pull Image from Docker Hub

```bash
docker pull vadalijahnavi/job-portal-backend:latest
```

For version `v1.0`:

```bash
docker pull vadalijahnavi/job-portal-backend:v1.0
```

## Docker Hub

Repository:

```text
vadalijahnavi/job-portal-backend
```

Available tags:

* `latest`
* `v1.0`

## Docker Workflow

```text
Dockerfile → docker build → Docker Image → docker run → Container → Application
```

## Conclusion

The Job Portal backend is containerized using Docker and can be built, run, tested, and pulled from Docker Hub.

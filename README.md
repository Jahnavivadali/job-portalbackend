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
  ## Pipeline

This project uses both **GitHub Actions** and **AWS CodePipeline** to automate the build and validation process.

### GitHub Actions

GitHub Actions is used for continuous integration. When changes are pushed to the `main` branch, the GitHub Actions workflow is triggered automatically. The workflow checks out the source code, installs the required dependencies, and performs the configured build or validation steps. This helps verify that the application can be processed correctly after a code change.

### AWS CodePipeline

AWS CodePipeline provides an automated pipeline in AWS. The source stage is connected to the GitHub repository using an AWS CodeConnections connection. When a new commit is pushed to the `main` branch, CodePipeline detects the change and starts a pipeline execution.

The source code is then passed to **AWS CodeBuild** for the build stage. CodeBuild reads the `buildspec.yml` file from the repository and executes the commands defined in it. The build process installs the required Python dependencies and performs the configured build or validation tasks.

### How They Work Together

GitHub Actions provides continuous integration checks for the repository, while AWS CodePipeline manages the AWS-based source and build process. When code is updated in GitHub, the workflows can automatically process the new changes. This reduces manual work and provides a consistent and repeatable development workflow.

The overall pipeline flow is:

```text
Developer Push
      ↓
GitHub Repository
      ↓
GitHub Actions
      ↓
AWS CodePipeline
      ↓
AWS CodeConnections
      ↓
AWS CodeBuild
      ↓
Build and Validation
```

## Docker Workflow

```text
Dockerfile → docker build → Docker Image → docker run → Container → Application
```

## Conclusion

The Job Portal backend is containerized using Docker and can be built, run, tested, and pulled from Docker Hub.

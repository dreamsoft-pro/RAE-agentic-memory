# ScreenWatcher - Corporate Edition

This is the production-ready, containerized deployment of the ScreenWatcher application.

## Prerequisites

- **Docker:** The entire application stack is orchestrated using Docker. You must have Docker and Docker Compose installed.
- **`.env` file:** Before starting the application, you must create a `.env` file in the project root. You can copy the provided example file:
  ```bash
  cp .env.example .env
  ```
- **Review `.env`:** Open the `.env` file and review the settings. For local development, the defaults are usually sufficient. For a production deployment, you **must** generate a new `SECRET_KEY` and configure `ALLOWED_HOSTS` and other security settings appropriately.

## Running the Application

The application stack is managed entirely through `docker-compose`.

### 1. Build and Start the Services

To build the Docker images and start all the services (web server, database, cache, Celery worker, and beat), run the following command in the project root:

```bash
docker-compose up --build -d
```
* The `--build` flag tells Docker Compose to build the images from the `Dockerfile`. You only need to use this the first time or when you change the application's dependencies or code.
* The `-d` (detached) flag runs the containers in the background.

### 2. Prepare the Database

After starting the services for the first time, you need to apply the database migrations and create a superuser account.

Run the migrations:
```bash
docker-compose exec web python manage.py migrate
```

Create a superuser to access the Django admin panel:
```bash
docker-compose exec web python manage.py createsuperuser
```
Follow the prompts to set up your admin username and password.

### 3. Accessing the Application

- **Web Application:** `http://localhost:8000`
- **Django Admin:** `http://localhost:8000/admin/`
- **API Documentation (Swagger UI):** `http://localhost:8000/api/schema/swagger-ui/`
- **Health Check:** `http://localhost:8000/healthz/`

### 4. Stopping the Application

To stop all running containers, use:

```bash
docker-compose down
```

## Running Tests and Linting

The project is equipped with a CI pipeline that runs tests and quality checks automatically. To run these checks locally, you can use the following commands.

### Running the Test Suite

Execute the test suite inside the `web` container:

```bash
docker-compose exec web pytest
```

### Checking Code Format and Style

Check for formatting issues with `black`:
```bash
docker-compose exec web black --check .
```

Check for linting errors with `flake8`:
```bash
docker-compose exec web flake8 .
```

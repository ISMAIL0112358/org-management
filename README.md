# Organization Management API

This project provides a multi-tenant organization management API built with FastAPI, PostgreSQL, and Alembic for database migrations. It allows for the creation and management of organizations, with separate administrative access for master administrators and individual organization administrators.

## API Overview and Journey

This API facilitates the creation and management of organizations. The typical journey involves a master administrator setting up new organizations, and then individual organization administrators managing their respective organizations.

### Endpoints:

#### 1. Master Admin Endpoints (Protected by Master Admin JWT)

These endpoints are for managing the overall system and creating new organizations. Access requires a JWT token obtained by logging in as a master administrator.

*   **`/master/register` (POST)**
    *   **Description:** Registers a new master administrator for the system.
    *   **Payload:**
        ```json
        {
          "admin": "master@example.com",
          "password": "master_password"
        }
        ```
    *   **Example `curl`:**
        ```bash
        curl -X POST "http://localhost:8000/master/register" \
        -H "Content-Type: application/json" \
        -d '{
          "admin": "master@example.com",
          "password": "master_password"
        }'
        ```

*   **`/master/login` (POST)**
    *   **Description:** Authenticates a master administrator and returns a JWT access token with a `master_admin` role.
    *   **Payload (Form Data):** `username=master@example.com&password=master_password`
    *   **Example `curl`:**
        ```bash
        curl -X POST "http://localhost:8000/master/login" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "username=master@example.com&password=master_password"
        ```
        *Copy the `access_token` from the response for subsequent master admin requests.*

*   **`/Org/create` (POST)**
    *   **Description:** Creates a new organization and its dedicated database. This endpoint requires a valid `master_admin` JWT token.
    *   **Payload:**
        ```json
        {
          "email": "admin@myorg.com",
          "password": "securepassword",
          "organization_name": "MyOrg"
        }
        ```
    *   **Example `curl`:**
        ```bash
        curl -X POST "http://localhost:8000/Org/create" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer YOUR_MASTER_ADMIN_JWT_TOKEN" \
        -d '{
          "email": "admin@myorg.com",
          "password": "securepassword",
          "organization_name": "MyOrg"
        }'
        ```

*   **`/Org/get` (POST)**
    *   **Description:** Retrieves details about a specific organization. This endpoint requires a valid `master_admin` JWT token.
    *   **Payload:**
        ```json
        {
          "organization_name": "MyOrg"
        }
        ```
    *   **Example `curl`:**
        ```bash
        curl -X POST "http://localhost:8000/Org/get" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer YOUR_MASTER_ADMIN_JWT_TOKEN" \
        -d '{
          "organization_name": "MyOrg"
        }'
        ```

#### 2. Organization Admin Endpoints

These endpoints are for administrators of specific organizations to log in and manage their organization's data (though no organization-specific data management endpoints are implemented yet).

*   **`/admin/login` (POST)**
    *   **Description:** Authenticates an administrator for a specific organization and returns a JWT access token.
    *   **Payload (Form Data):** `username=admin@myorg.com&password=securepassword`
    *   **Example `curl`:**
        ```bash
        curl -X POST "http://localhost:8000/admin/login" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "username=admin@myorg.com&password=securepassword"
        ```

## Packages Used

This project utilizes the following key Python packages:

*   **`fastapi`**: A modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints. Chosen for its speed, automatic interactive API documentation (Swagger UI/Redoc), and ease of use.
*   **`uvicorn`**: An ASGI server, necessary to run FastAPI applications. It's a fast and lightweight server.
*   **`pydantic`**: Used for data validation and settings management. It allows defining data schemas with type hints, ensuring incoming request data is valid and structured correctly.
*   **`pydantic-settings`**: A Pydantic extension for managing application settings, especially for loading configuration from environment variables and `.env` files. This promotes secure and flexible configuration.
*   **`passlib[bcrypt]`**: Provides secure password hashing and verification using the bcrypt algorithm, crucial for storing user passwords safely.
*   **`python-jose[cryptography]`**: A comprehensive library for JSON Web Token (JWT) handling, used for creating, encoding, and decoding JWTs for authentication and authorization.
*   **`psycopg2-binary`**: A PostgreSQL adapter for Python, enabling the application to connect and interact with PostgreSQL databases.
*   **`alembic`**: A lightweight database migration tool for SQLAlchemy. It allows for version-controlled database schema changes, making it easy to evolve the database structure over time.
*   **`SQLAlchemy`**: A powerful and flexible SQL toolkit and Object-Relational Mapper (ORM). While not directly used as an ORM for all database interactions in this project, it's a core dependency for Alembic to define database models and generate migrations.
*   **`python-dotenv`**: Used to load environment variables from a `.env` file into `os.environ`, simplifying local development by keeping sensitive credentials out of the codebase.

## How to Run with Docker

To run this application using Docker, follow these steps:

### Prerequisites

*   [Docker](https://docs.docker.com/get-docker/) installed on your system.

### Steps

1.  **Create a `.env` file:**
    Ensure you have a `.env` file in the root directory of your project with the following content. Replace `your_jwt_secret` and `1234` with your desired values.

    ```dotenv
    SECRET_KEY="your_jwt_secret"
    MASTER_DB_NAME="masterdb"
    MASTER_DB_USER="postgres"
    MASTER_DB_PASSWORD="1234"
    MASTER_DB_HOST="db" # This will be the service name in docker-compose
    MASTER_DB_PORT="5432"
    ```

2.  **Run with Docker Compose:**
    Navigate to the root directory of your project (where `docker-compose.yml` is located) in your terminal and run:

    ```bash
    docker-compose up --build
    ```
    This command will:
    *   Build the Docker image for your application (if it's not already built or if changes are detected).
    *   Start the PostgreSQL database service.
    *   Start your FastAPI application service.
    *   Create a network for the services to communicate.

3.  **Access the API:**
    Once the containers are running, the API will be accessible at `http://localhost:8000`.

    You can then use the `curl` commands provided in the "API Overview and Journey" section to test the endpoints.

**Important Notes:**

*   **Database Persistence:** The `pg_data` volume in `docker-compose.yml` ensures that your PostgreSQL data persists even if you stop and restart the containers. This means your organizations and master admin data will not be lost.
*   **Stopping Containers:** To stop the running containers, press `Ctrl+C` in the terminal where `docker-compose up` is running. To stop and remove the containers, networks, and volumes (but keep `pg_data` volume by default), run `docker-compose down`.
*   **Database Migrations:** After starting the services for the first time, you will need to run Alembic migrations to set up your database schema. You can do this by executing the migration command within the running `app` container:
    ```bash
    docker-compose exec app alembic upgrade head
    ```
    This command will apply all pending migrations to your PostgreSQL database running in the `db` container.

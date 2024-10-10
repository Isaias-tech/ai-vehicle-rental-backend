# AIVehicleRental

Description

## Technologies

This project uses the following technologies:

### Backend
- **Python 3.12**: The programming language used for the backend.
- **Poetry 1.8.3**: A dependency manager used to handle Python package installations and environments.
- **Brain tree 4.30.0**: A library for integrating Braintree payment gateway into the project, allowing support for PayPal and credit card transactions.
- **Django 5.1.1**: A high-level Python web framework used for building the web application and API.
- **Django REST Framework (DRF) 3.15.2**: A powerful toolkit for building Web APIs in Django.
- **Django REST Framework SimpleJWT 5.3.1**: Used for handling JWT-based authentication in the API.
- **Gunicorn 23.0.0**: A Python WSGI HTTP server for running the Django application in production.
- **Whitenoise 6.7.0**: A tool for managing and serving static files in a production environment.
- **CORS Headers 4.4.0**: A Django extension for enabling Cross-Origin Resource Sharing (CORS), allowing the API to be accessed from other domains.
- **Python-dotenv 1.0.1**:  A library for loading environment variables from a .env file.
- **dj-database-url 2.2.0**: A helper library that simplifies setting up the database connection using a URL.

### Development
- **Black 24.8.0**: A code formatter for enforcing consistent style across the Python codebase.
- **Flake8 7.1.1**: A linting tool used to ensure code quality by checking for common Python errors.
- **Pre-commit 3.8.0**: A framework for managing and automating Git pre-commit hooks to ensure code quality before committing changes.

## Contribution Guidelines

To ensure the project maintains high quality and consistency, it is a must to follow these instructions when contributing.

### 1. Branch Naming Convention

When working on a new feature, bug fix, or any other change, create a new branch. Follow these naming conventions:

- **Features**: `feature/short-description`
- **Bug Fixes**: `fix/short-description`
- **Documentation**: `docs/short-description`
- **Chore**: `chore/short-description`

Examples:
- `feature/user-authentication`
- `fix/login-bug`
- `docs/update-readme`
- `chore/setup-linting`

### 2. Commit Message Convention

Follow the **conventional commits** format for writing commit messages. This ensures that commit history is readable and helps in generating release notes automatically.

The format is:

```
<type>: <subject>
```

Types of commits:
- **Feat**: Introduces a new feature.
- **Fix**: Fixes a bug or issue.
- **Docs**: Updates or adds documentation.
- **Style**: Changes code style or formatting (doesn't affect functionality).
- **Refactor**: Refactors code without adding features or fixing bugs.
- **Test**: Adds or modifies tests.
- **Chore**: Changes related to the build process or auxiliary tools.

Examples:
- `feat: add JWT authentication for users`
- `fix: resolve issue with user login timeout`
- `docs: update API documentation for user endpoints`
- `style: reformat code to follow PEP8`
- `test: add unit tests for profile update feature`

### 3. Install Pre-commit Hooks

The project uses **pre-commit** hooks to ensure code quality before committing. Make sure you have the hooks installed and configured:

1. Install **pre-commit** hooks:

   ```bash
   poetry run pre-commit install
   ```

2. Every time you commit, **pre-commit** will automatically run checks like formatting with **black**, linting with **flake8**, and more.

3. To manually run all hooks against all files:

   ```bash
   poetry run pre-commit run --all-files
   ```

Make sure to fix any issues reported by the hooks before pushing your changes.

### 4. Code Style and Linting

Follow these rules for maintaining consistent code quality:

- **Code Formatting**: The project uses **Black** for code formatting. Ensure your code is formatted before pushing:

  ```bash
  poetry run black .
  ```

- **Linting**: Lint your code using **Flake8** to ensure there are no syntax or style issues:

  ```bash
  poetry run flake8 .
  ```

### 5. Create Pull Requests

Once your changes are ready:

1. **Push** your branch to the repository:
   ```bash
   git push origin <branch-name>
   ```

2. **Create a Pull Request**:
   - Go to the repository on GitHub.
   - Click the **Compare & pull request** button.
   - Provide a clear description of what your changes do and any relevant issue references.

3. **Ensure that your pull request adheres to the following**:
   - Descriptive title (e.g., "Fix user authentication bug").
   - Links to relevant issues (if applicable).
   - A brief summary of the changes and why they were made.

### 6. Code Review and Feedback

Once your pull request is submitted:

- **Address Feedback**: If reviewers suggest changes, address them promptly and update your pull request.
- **Keep Commits Clean**: Make sure to squash any "fix" commits (e.g., fixing typos) before the final merge to keep the commit history clean.

### 7. Avoid Large Pull Requests

Try to keep your pull requests small and focused on one task at a time. Large pull requests can be difficult to review and understand.

### 8. Update Postman Collection

If a new URL path is added or an existing URL, view, model, or serializer is modified, make sure to update the Postman collection. This ensures that the next developer has the most up-to-date tests for the API endpoints.

### Summary of Contribution Workflow

1. Clone the repository.
2. Create a new branch based on the task (feature, fix, chore, etc.).
3. Write meaningful commit messages following the `Feat:`, `Fix:`, etc., format.
4. Install and run pre-commit hooks before committing.
5. Ensure the code passes all linters.
6. Push your changes to your branch.
7. Create a pull request and link relevant issues.
8. Respond to feedback and make improvements.

### Key Points:
- **Branch Naming**: Follows a clear structure like `feature/`, `fix/`, `docs/`, etc.
- **Commit Messages**: Use conventional commit messages like `Feat:`, `Fix:`, `Docs:`.
- **Pre-commit Hooks**: Ensure code quality with pre-commit hooks before committing.
- **Pull Requests**: Keep pull requests focused, descriptive, and small.


## Environment variables

| Environment Variable | Description |
| :--- | :--- |
| `DJANGO_SECRET_KEY` | **Development and Production** The secret key used for cryptographic signing in Django. Keep this value secure and confidential. |
| `DEBUG` | Set to `True` to enable debug mode in Django (only for development). Set to `False` in production. |
| `DEVELOPMENT_MODE` | Set to `True` to enable development mode in Django (only for development). Set to `False` in production. |
| `ALLOWED_HOSTS` | A comma-separated list of allowed host/domain names for your Django app. Example: `localhost,127.0.0.1`. |
| `CORS_ALLOWED_ORIGINS` | A comma-separated list of origins allowed to make cross-site HTTP requests. Example: `http://localhost:3000`. |
| `DATABASE_URL` | **Only for production** The database connection URL (typically for PostgreSQL). Example: `postgres://user:password@localhost:5432/mydb`. |
| `FRONTEND_URL` | The frontend url. |
| `MAILGUN_DOMAIN` | The domain used to send emails through Mailgun. This is the custom domain that was registered with Mailgun to send emails. |
| `MAILGUN_API_KEY` | The **API key** provided by Mailgun to authenticate and send emails using the Mailgun service. |
| `SERVER_DOMAIN` | The domain where the Django application is hosted. This is used in constructing absolute URLs, such as for sending email confirmation links. |
| `BRAINTREE_ENVIRONMENT` | The environment for Braintree transactions, `Sandbox` for testing or `Production` for live transactions. |
| `BRAINTREE_MERCHANT_ID` | The unique identifier for your Braintree merchant account. |
| `BRAINTREE_PUBLIC_KEY` | The public key provided by Braintree for API authentication. |
| `BRAINTREE_PRIVATE_KEY` | The private key provided by Braintree for API authentication. |

## How to Install and Run the Project Locally

### Prerequisites

Before you begin, ensure that you have the following installed:

- **Python 3.12+**: [Download Python](https://www.python.org/downloads/)
- **Poetry**: [Install Poetry](https://python-poetry.org/docs/#installation)
- **Poetry Export**: [Install Poetry Export](https://github.com/python-poetry/poetry-plugin-export)

### 1. Clone the Repository

Start by cloning the project repository from GitHub:

```bash
git clone https://github.com/Isaias-tech/ai-vehicle-rental-backend.git
cd ai-vehicle-rental-backend
```

### 2. Install Dependencies

Use **Poetry** to install all project dependencies, as defined in the `pyproject.toml` file:

```bash
poetry install
```

This command will install both production and development dependencies.

### 3. Set Up Environment Variables

Create a `.env` file in the project root directory and add the environment variables explained in the [Environment Variables](#environment-variables) section.

### 4. Apply Migrations

Once the database is set up, apply the Django migrations to initialize the database schema:

```bash
poetry run python manage.py migrate
```

### 5. Run the Development Server

Start the Django development server to run the project locally:

```bash
poetry run python manage.py runserver
```

The development server will start at `http://localhost:8000/`.

### 6. Pre-commit Hooks (For Development)

If you're contributing to the project, ensure that **pre-commit** hooks are installed. These hooks will automatically check code formatting and quality before allowing commits:

```bash
poetry run pre-commit install
```

You can also manually run the pre-commit hooks to check code quality:

```bash
poetry run pre-commit run --all-files
```

### 7. Access the Application

Once the development server is running, you can access the application by navigating to:

```
http://localhost:8000/
```

You can interact with the API endpoints through tools like **Postman** and importing the `ai-vehicle-rental.postman_collection.json` file on the repository that has a list of common test cases.

Now you should be ready to run and test the project locally.

## How to Deploy and Run the Project in Production

### Prerequisites

Before deploying the project in production, ensure that you have the following installed:

- **Docker**: [Install Docker](https://docs.docker.com/get-docker/)
- **Database String**: It can be any database supported by [dj-database-url](https://pypi.org/project/dj-database-url/) library.

### 1. Set Up Environment Variables

In production, you only need to define the **`DATABASE_URL`** environment variable. This can be done via your hosting platform or Docker environment configuration.

The `DATABASE_URL` format for PostgreSQL looks like this:

```env
DATABASE_URL=postgres://user:password@host:port/dbname
```

Replace:
- `user` with your database username.
- `password` with your database password.
- `host` with your database host (e.g., `localhost` or the database server IP).
- `port` with your database port (default PostgreSQL port is `5432`).
- `dbname` with the name of your production database.

### 2. Build the Docker Image

To build the Docker image for your project, navigate to the project root directory (where the `Dockerfile` is located) and run the following command:

```bash
docker build -t ai-vehicle-rental-backend.
```

This command builds the Docker image using the provided `Dockerfile` and tags it as `ai-vehicle-rental-backend`.

### 3. Run the Docker Container

Once the image is built, run the container, making sure to pass in the `DATABASE_URL` environment variable.

```bash
docker run -d --name ai-vehicle-rental-backend -e "DATABASE_URL=postgres://user:password@host:port/dbname" -p 8000:8000 ai-vehicle-rental-backend
```

- `-d`: Runs the container in detached mode (in the background).
- `--name ai-vehicle-rental-backend`: Names the container `ai-vehicle-rental-backend` for easy reference.
- `-e DATABASE_URL=...`: Sets the environment variable for the database URL.
- `-p 8000:8000`: Maps port `8000` from the container to port `8000` on the host machine.
- `ai-vehicle-rental-backend`: The name of the Docker image built earlier.

### 4. Access the Application

Once the container is running, your Django project will be available on:

```
http://localhost:8000/
```

You can interact with the API endpoints through tools like **Postman** and importing the `ai-vehicle-rental.postman_collection.json` file on the repository that has a list of common test cases.

### 5. (Optional) Stopping and Restarting the Container

If you need to stop the container, run:

```bash
docker stop ai-vehicle-rental-backend
```

To restart the container:

```bash
docker start ai-vehicle-rental-backend
```

### 6. (Optional) Checking Logs

To view the logs from the running container, use:

```bash
docker logs ai-vehicle-rental-backend
```

### Summary of Steps:

1. **Set Environment Variables**: Only the `DATABASE_URL` is needed.
2. **Build the Docker Image**: Use `docker build`.
3. **Run the Docker Container**: Use `docker run` and pass in the `DATABASE_URL`.
4. **Access the Application**: The app will be available at `http://localhost:8000/`.

# Flask Report Services Backend

Backend service for the **Report SA Services** application. This repository contains a Flask API backed by SQLite, with functionality for products, agents, clients, sales, payments, inventory history, and report generation.

The application is containerized with Docker so it can run with a consistent Python environment without requiring Python or the project dependencies to be installed directly on the host machine.

## Overview

The backend uses:

- **Python 3.10**
- **Flask**
- **Flask-CORS**
- **SQLite**
- **OpenPyXL** for Excel report generation
- **LibreOffice** for headless Excel-to-PDF conversion
- **Docker**

## Repository Structure

```text
.
├── app.py
├── __init__.py
├── requirements.txt
├── controllers/
│   ├── app_definition.py
│   ├── db.py
│   ├── reportes.py
│   └── ...
├── reportes/
│   └── base/
│       └── Excel report templates
├── instance/
├── addSummarytable.py
├── msa.db
└── .gitignore
```

The exact contents of `controllers/` may change as the application evolves.

## Getting Started

### Prerequisites

Install:

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Git

Python does not need to be installed on the host machine because the backend runs inside Docker.

Verify Docker:

```bash
docker --version
```

## Build the Docker Image

From the repository root:

```bash
docker build -t my-flask-backend .
```

This uses the repository's `Dockerfile` to create the application image, install the Python dependencies, and install the tools required for report generation.

## Run the Backend

The application exposes port `5000`.

For persistent application data, map host directories to the container:

```bash
docker run --name my-flask-backend \
  -p 5000:5000 \
  -v "<host-reports-directory>:/app/generated_reports" \
  -v "<host-database-directory>:/app/data" \
  my-flask-backend
```

Replace:

```text
<host-reports-directory>
```

with the directory where generated reports should be stored, and:

```text
<host-database-directory>
```

with the directory containing the SQLite database.

For example, a project could use a structure like:

```text
project-data/
├── reports/
└── database/
    └── msa.db
```

The important container mappings are:

```text
Host reports directory  -> /app/generated_reports
Host database directory -> /app/data
```

This keeps generated data outside the Docker image.

## Why Mount the Database?

The SQLite database contains application state and should not depend on the lifecycle of the Docker image.

The application uses:

```text
/app/data/msa.db
```

inside the container.

That directory should be mapped to a persistent directory on the host.

This provides an important separation:

```text
Docker image
├── Application code
├── Python dependencies
├── LibreOffice
└── Report templates

Host / mounted storage
├── SQLite database
└── Generated reports
```

Rebuilding the Docker image therefore does not replace the active database.

## Database Configuration

Database access is centralized in `controllers/db.py`.

The application uses a configurable database path:

```python
DB_PATH = os.getenv("DB_PATH", "/app/data/msa.db")

def get_db_connection():
    return sqlite3.connect(DB_PATH)
```

Database operations should use:

```python
get_db_connection()
```

instead of hard-coded database paths.

This allows the same codebase to work in Docker and in other environments.

## Report Generation

The backend generates Excel reports with OpenPyXL and converts them to PDF with LibreOffice.

The general flow is:

```text
API request
    |
    v
Load report template
    |
    v
Generate .xlsx
    |
    v
Save to /app/generated_reports
    |
    v
Convert with LibreOffice
    |
    v
Generate .pdf
```

### Report Templates

Report templates are stored in the repository under:

```text
reportes/base/
```

The templates remain inside the Docker image.

Generated reports are stored separately under:

```text
/app/generated_reports
```

and are mapped to a host directory.

Do not mount the host reports directory over `/app/reportes`, because doing so would hide the templates included in the image.

## PDF Page Scaling

Reports can use spreadsheet page setup to fit the report width when converting to PDF.

For example:

```python
def configurePrintSettings(sheet):
    sheet.page_setup.fitToWidth = 1
    sheet.page_setup.fitToHeight = 0
    sheet.sheet_properties.pageSetUpPr.fitToPage = True
```

This fits all columns to one page wide while allowing the report to continue vertically across multiple pages.

## API

The Flask application exposes endpoints for areas such as:

- Products
- Agents
- Clients
- Sales
- Payments
- Inventory
- Reports

The API uses standard HTTP methods including:

```text
GET
POST
PUT
DELETE
```

Endpoint definitions are located in the Flask application code under `controllers/`.


## Viewing Logs

Because Flask runs inside Docker, application `print()` output is written to the container logs.

Follow the logs with:

```bash
docker logs -f my-flask-backend
```

This is useful for debugging application startup, API activity, and report generation.

## Useful Docker Commands

### Build

```bash
docker build -t my-flask-backend .
```

### Run

```bash
docker run --name my-flask-backend \
  -p 5000:5000 \
  -v "<host-reports-directory>:/app/generated_reports" \
  -v "<host-database-directory>:/app/data" \
  my-flask-backend
```

### Stop

```bash
docker stop my-flask-backend
```

### Start an existing container

```bash
docker start my-flask-backend
```

### Remove a container

```bash
docker rm my-flask-backend
```

### View running containers

```bash
docker ps
```

### View all containers

```bash
docker ps -a
```

### View logs

```bash
docker logs -f my-flask-backend
```

### Open a shell inside the container

```bash
docker exec -it my-flask-backend bash
```

### Check LibreOffice

```bash
docker exec my-flask-backend libreoffice --version
```

## Rebuilding After Code Changes

After modifying backend code:

```bash
docker build -t my-flask-backend .
```

If a container using the previous image already exists:

```bash
docker stop my-flask-backend
docker rm my-flask-backend
```

Then run the new image again using the same volume mappings.

Because the database and generated reports are stored outside the image, rebuilding does not replace those mounted files.

## Development Notes

### Keep code and mutable data separate

The Docker image should contain the application and its runtime dependencies.

Mutable data such as the SQLite database and generated reports should live in mounted host directories.

This makes rebuilding and recreating containers safer.

### Windows-specific Excel automation

The original application contains Windows-specific modules such as:

```python
win32com.client
pythoncom
winshell
```

These are not suitable for Linux containers.

The containerized version therefore uses LibreOffice for Excel-to-PDF conversion instead of Windows Excel COM automation.

## Future Improvements

Potential future improvements include:

- Add a `.dockerignore` file so files such as the local SQLite database are not copied into the image.
- Add `docker-compose.yml` to simplify building and starting the application.
- Move additional configuration values to environment variables.
- Replace SQL string interpolation with parameterized queries.
- Add automated API and report-generation tests.
- Add a container health check.
- Use a production WSGI server for production deployments.
- Containerize the React frontend and connect it to the backend through Docker networking.

## License

Add the appropriate project license here.

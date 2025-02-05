# Dapr Testcontainers Sample

This repository demonstrates how to build a simple pub-sub application using [Dapr](https://dapr.io/) and test it with [Testcontainers](https://testcontainers-python.readthedocs.io/) for Python. It consists of two services:

1. **Order Publisher** (FastAPI-based)
2. **Order Processor** (Flask-based)

Each service is containerized with Docker and can be run either locally or within a test environment spun up by Testcontainers.

---

## Prerequisites

1. [Python 3.11+](https://www.python.org/downloads/) (the example uses Python 3.11 Slim in its Docker images, but you can run locally with other versions of 3.x).
2. [Docker](https://docs.docker.com/get-docker/)
3. (Optional) [Dapr CLI](https://docs.dapr.io/getting-started/install-dapr-cli/) if you want to run each service locally using Dapr directly.

---

## Project Layout

A quick summary of the repository structure:

```
dapr-testcontainers-blog/
├── .vscode/             # VS Code debug and tasks configurations
├── dapr-components/     # Dapr components (pubsub, etc) for local dev
├── order-processor/     # Order Processor service (Flask)
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
├── order-publisher/     # Order Publisher service (FastAPI)
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
├── tests/
│   ├── conftest.py      # Pytest fixtures using Testcontainers
│   ├── test_orders.py   # Example tests for pub-sub
│   ├── docker-images/   # Dockerfiles used for test images
│   ├── pytest.ini       # Pytest configuration
│   └── requirements.txt # Python dependencies for testing
├── sample.http          # Sample HTTP request to publish an order
└── README.md            # You're reading it now!
```

---

## 1. Create and Activate a Virtual Environment

It is best practice to use a virtual environment to isolate your Python dependencies:

1. Open a terminal in the root of the repository (`dapr-testcontainers-blog/` folder).
2. Create a virtual environment:

   On macOS/Linux:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

   On Windows (PowerShell):
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

3. Confirm your environment is active (your prompt typically shows `(.venv)`).

---

## 2. Install Dependencies

### 2.1 Install Local Application Dependencies

If you want to run the Publisher and Processor services locally, install their dependencies:

```bash
pip install -r order-publisher/requirements.txt
pip install -r order-processor/requirements.txt
```

### 2.2 Install Test Dependencies

In order to run tests (which use Testcontainers), install the test dependencies:

```bash
pip install -r tests/requirements.txt
```

---

## 3. Running the Services Locally (Optional)

If you want to run and test each service locally with Dapr manually, you can do so, but will need a local Redis or other pub/sub. For a minimal approach, run each service directly without Dapr sidecars:

### 3.1 Order Processor

```bash
cd order-processor
python app.py
```

This starts the Flask service on port 8001 (by default).

### 3.2 Order Publisher

Open another terminal, activate the same or another virtual environment, then:

```bash
cd order-publisher
uvicorn app:app --host 0.0.0.0 --port 8000
```

Using the sample HTTP request in `sample.http`:

```http
POST http://localhost:8000/order
Content-Type: application/json

{
  "id": 123,
  "customer": "Sample Customer"
}
```

You can send this request via an HTTP client (like REST Client VSCode extension or curl/Postman).

---

## 4. Run the Tests

This setup uses Testcontainers to dynamically build Docker images and start the required containers (Publisher, Processor, Redis, etc.) in an isolated network. You don’t need to manually spin up containers. Just run:

```bash
pytest
```

Pytest will:
1. Build the base Docker images for both services (`publisher:latest` and `processor:latest`).
2. Build the test images that include Dapr and the app (`publisher:integration` and `processor:integration`).
3. Spin up an isolated Redis container (for pub-sub).
4. Spin up the Publisher and Processor containers (with Dapr sidecars).
5. Run the test suite in `tests/test_orders.py`.
6. Tear down all containers on test completion.

---

## 5. VS Code Integration

For convenience, this repository includes several VS Code configuration files in the `.vscode/` folder:

- `launch.json` defines debug configurations for the Publisher and Processor.
- `tasks.json` sets up and tears down Dapr sidecars as pre/post debug tasks.
- `settings.json` configures Python for testing with Pytest.

If you use VS Code, you can simply open this folder, select the debug configuration you want (e.g., “Order publisher” or “Order processor”), and start debugging.

---

## 6. Useful Commands

Below are some commands you may find helpful along the way:

1. Create virtual environment (once):
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r tests/requirements.txt
   ```
3. Run tests:
   ```bash
   pytest
   ```
4. Build & run Docker images manually (if desired):
   ```bash
   # Publisher
   docker build -t publisher:latest ./order-publisher
   docker run -p 8000:8000 --name publisher --rm publisher:latest

   # Processor
   docker build -t processor:latest ./order-processor
   docker run -p 8001:8001 --name processor --rm processor:latest
   ```
5. Check logs from containers (if you used Docker or Testcontainers) to see request details.

---

## 7. Cleaning Up

If you’ve run containers manually, you can stop them with:
```bash
docker stop <container_name>
```
If you ran tests with Pytest, the containers are automatically cleaned once the tests complete.

---

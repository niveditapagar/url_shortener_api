# URL shortener API

This repository contains the API implementation for a URL shortener app using FastAPI and PostgreSQL.

## Installation

### Prerequisites

- Python 3.7+
- pip
- postgresql

### Setup

1. Clone the repository

1. Navigate to the project directory:
    ```bash
    cd url_shortener_api
    ```
1. Create a virtual environment or poetry environment 
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

1. Install the project dependencies by running:
    ```bash
    make install
    ```

## Usage

### Run the Application

1. **Create a Database:**
    - Before running the application, create a new PostgreSQL database with the desired name. Note down the database name as you will need it in the next steps.

1. **Create an Environment Configuration File:**
    - Create a `.env` file in your project directory. This file will contain environment-specific configurations.
    - Add the following configurations to your `.env` file. You can adjust the values to match your environment:

    ```plaintext
    ENV_NAME="Dev"
    BASE_URL="http://127.0.0.1:8000"
    DB_URL="postgresql://username:password@localhost:5432/your-database-name"
    ```

    Replace `username`, `password`, and `your-database-name` with your database credentials and database name. Ensure the `DB_URL` matches your database configuration.

1. **Update Configuration:**
    - Open the `config.py` file in your project directory.
    - Update the `DB_URL` parameter 

1. **Note:** The "urls" table required for the URL shortener will be automatically created by the application when it starts up. You do not need to create it manually.

1. To run the application, use the following command:
    ```bash
    make run
    ```

1. Visit the following URL to test your solution:
    ```bash
    http://127.0.0.1:8000
    ```

1. Then visit /docs for a detailed look at the Swagger documentation and to try out the API functionality.
    ```bash
    http://127.0.0.1:8000/docs
    ```
    * Expand the /url endpoint and click on "Try it out."
    * Replace the "string" in the request body with a URL and click "Execute" to get the shortened URL.
    * You can use the shortened url to visit the page

### Run tests

To run the tests, execute the following command:

```bash
make test
```
This python service will be used to manage user authentication and validation.

## Installation

### MySQL Database

A MySQL server is used for persistent storage of user login details.

The database schema can be found in `schema.sql`.

A Docker image is provided for this database.

```
docker build -f sql.Dockerfile -t mysql .
docker run -p 3306:3306 mysql
```

### Redis Session Cache

A Redis server is used to store ephemeral user sessions.

```
docker run redis:alpine redis-server --requirepass yourpasswordkkfkfa
```

### Python Server

Requires Python 3.11+

```
python -m pip install -r requirements.txt
python -m uvicorn http_server:app --host 0.0.0.0 --port 8080
```
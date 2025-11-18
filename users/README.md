This python service will be used to manage user authentication and validation.

## Installation

Requires Python 3.11+

```
python -m pip install -r requirements.txt
python -m uvicorn http_server:app --host 0.0.0.0 --port 8080
```
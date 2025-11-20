import os
import json
import copy
import uuid
import redis
import logging
import aiomysql
import nacl.hash
from pydantic import BaseModel

from fastapi import FastAPI, Request, Depends, HTTPException, Response, Cookie
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS
origins = [
    "http://127.0.0.1",
    "http://localhost"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Set-Cookie"]
)

db_config = {
    "host": os.environ.get("DB_HOST", "127.0.0.1"),
    "user": os.environ.get("DB_USER", "root"),
    "password": os.environ.get("DB_PASS", "kjndsfdsndsn"),
    "db": os.environ.get("DB_NAME", "db"),
    "port": 3306,
    "autocommit": True
}

async def get_db():
    config = copy.deepcopy(db_config)
    config["cursorclass"] = aiomysql.cursors.DictCursor
    conn = await aiomysql.connect(**config)
    try:
        yield conn
    finally:
        conn.close()

class UserSession:
    def __init__(self):
        self.session_storage_client = redis.StrictRedis(host=os.environ.get("CACHE_HOST", "localhost"), port=6379, db=0, password="yourpasswordkkfkfa")

    def makeNewUserSession(self, username):
        session_id = str(uuid.uuid4())
        self.session_storage_client.set(session_id, json.dumps({"username": username}))
        return session_id

    def getUserFromSession(self, session_id):
        return json.loads(self.session_storage_client.get(session_id).decode())["username"]

def get_sessions():
    session_storage = UserSession()
    yield session_storage

def hash_password(password):
    SALT = "appsalt"
    password + SALT
    return nacl.hash.sha256(password.encode()).decode()

# route handlers
@app.get("/")
def root():
    return "User service"

# User Registration/Creation Route
class RegistrationRequest(BaseModel):
    username: str
    email: str
    password: str
@app.post("/users/register")
async def user_register(request:RegistrationRequest, rds_client=Depends(get_db)):
    async with rds_client.cursor() as cur:
        await cur.execute("""
            INSERT IGNORE INTO users (username, email, password)
                VALUES (%s, %s, %s)
        """, (request.username, request.email, hash_password(request.password)))
    

# User Login Route
class LoginRequest(BaseModel):
    username: str
    password: str
@app.post("/users/login")
async def user_login(request:LoginRequest, response:Response, rds_client=Depends(get_db), session_storage=Depends(get_sessions)):
    # verify password is correct
    # hash the input - the data is hashed in the database
    hashed_password = hash_password(request.password)
    # compare the hashes
    async with rds_client.cursor() as cur:
        await cur.execute("""
            SELECT * FROM users
            WHERE (username, password) = (%s, %s)
            """, (request.username, hashed_password))
        user_result_row = await cur.fetchone()
    if not user_result_row:
        raise HTTPException(status_code=401)
    # add Redis entry {session_id:username} with 2 hour timeout
    session_id = session_storage.makeNewUserSession(request.username)
    # return session id in response body and cookie
    response.set_cookie(key="session_id", value=session_id)

@app.post("/users/logout")
async def users_logout(response:Response, session_id:str=Cookie(None), session_storage=Depends(get_sessions)):
    # destroy sessioroutern by deleting session entry from Redis
    if not session_id:
        return
    session_storage.session_storage_client.delete(session_id)
    # and deleting the session cookie from the client
    response.delete_cookie(key="session_id")

@app.get("/users/whoami")
async def users_whoami(session_id:str=Cookie(None), rds_client=Depends(get_db), session_storage=Depends(get_sessions)):
    if not session_id:
        return
    username = session_storage.getUserFromSession(session_id)
    async with rds_client.cursor() as cur:
        await cur.execute("""
            SELECT username, email
            FROM users
            WHERE username = %s
            """, (username))
    return await cur.fetchone()
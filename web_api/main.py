from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import sqlite3

app = FastAPI()
SECRET_KEY = "a_very_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

hashed_admin_password = get_password_hash("admin")


@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):

    if form_data.username != "admin" or not verify_password(form_data.password, hashed_admin_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise Exception
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return username
def get_db_connection():
    conn = sqlite3.connect('../ram_data.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/ram_data/")
async def protected_data(current_user: str = Depends(get_current_user), n: int):
    if n <= 0:
        raise HTTPException(status_code=400, detail="n must be greater than 0")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT total, used, free, timestamp FROM ram ORDER BY timestamp DESC LIMIT ?
    ''', (n,))
    rows = cursor.fetchall()
    print(rows)
    conn.close()

    return [{"total": row["total"], "used": row["used"], "free": row["free"], "timestamp": row["timestamp"]} for row in
            rows]


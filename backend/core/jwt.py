from datetime import datetime, timedelta
from jose import jwt, JWTError

SECRET_KEY="gupt-chavi"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_TIME=30

def create_token(data: dict, expries_time: timedelta | None=None):
    to_encode=data.copy()
    expires=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_TIME)
    

    to_encode.update({"exp": expires})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def to_decode(token: str):
    try:
        payload=jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
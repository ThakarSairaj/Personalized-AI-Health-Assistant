from passlib.context import CryptContext

pwd_cryp=CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(plain_password: str) -> str:
    return pwd_cryp.hash(plain_password)

def verify_password(plain_password: str, database_password: str)-> bool:
    return pwd_cryp.verify(plain_password, database_password)
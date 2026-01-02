from passlib.context import CryptContext

pwd_cryp=CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(plain_password: str) -> str:
    return pwd_cryp.hash(plain_password)
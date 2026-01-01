from passlib.context import CryptContext

pwd_cryp=CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(plain_password: str) -> str:
 
    if not isinstance(plain_password, str):
        raise ValueError(f"Password must be a string, got {type(plain_password)}")
    
   
    truncated = plain_password.encode("utf-8")[:72].decode("utf-8", errors="ignore")
    
    return pwd_cryp.hash(truncated)
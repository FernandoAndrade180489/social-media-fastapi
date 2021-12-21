from passlib.context import CryptContext

# To hash password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)


# To validate if password sent to login function is the same of hashed on database
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
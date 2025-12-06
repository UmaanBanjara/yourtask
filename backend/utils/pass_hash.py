from passlib.context import CryptContext


pwd_context = CryptContext(schemes=['bcrypt']) #context schema


def hash_pass(plain_pass : str) -> str:
    hashedPassword = pwd_context.hash(plain_pass[:72])
    return hashedPassword

def verify_pass (plain_pass : str , hashed_pass : str) -> bool:
    verifiedPassword = pwd_context.verify(plain_pass , hashed_pass)
    return verifiedPassword


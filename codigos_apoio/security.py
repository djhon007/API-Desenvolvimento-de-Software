from passlib.context import CryptContext

#criptografia senha
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


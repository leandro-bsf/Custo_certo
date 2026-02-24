import jwt
from datetime import datetime, timedelta

SECRET_KEY = "zxkcODy3Z4fvZCKHzoDaFkXI6LepIATFBkdeSKS8Z50"
ALGORITHM = "HS256"
EXPIRATION_MINUTES = 60


def criar_token(usuario_id, email):
    payload = {
        "sub": usuario_id,
        "email": email,
        "exp": datetime.utcnow() + timedelta(minutes=EXPIRATION_MINUTES)
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def validar_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
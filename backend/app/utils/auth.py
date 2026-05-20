import jwt
import datetime

SECRET_KEY = "wayne-secret-key"

def gerar_token(user):
    payload = {
        "user_id": user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


def validar_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["user_id"]
    except:
        return None
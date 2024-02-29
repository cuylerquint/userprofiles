import datetime

import jwt
from django.conf import settings


def get_user_access_token(exp_days=45):
    return jwt.encode(
        {
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=exp_days),
            "is_admin": False,
        },
        settings.SECRET_KEY,
        algorithm="HS256",
    ).decode('utf-8')



import datetime

from config.env import env

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": datetime.timedelta(minutes=int(env.ENVIRON['JWT_ACCESS_TOKEN_LIFETIME'])),
    "REFRESH_TOKEN_LIFETIME": datetime.timedelta(minutes=int(env.ENVIRON['JWT_REFRESH_TOKEN_LIFETIME'])),
}


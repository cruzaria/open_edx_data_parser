import os

from web.utils import random_token


USER_TOKEN = random_token(16)

envs = {
    'host': os.environ['OE_MYSQL_HOST'],
    'user': os.environ['OE_MYSQL_USER'],
    'pass': os.environ['OE_MYSQL_PASS'],
    'db': os.environ['OE_MYSQL_DB'],
    'token': os.environ['OE_TOKEN']
}
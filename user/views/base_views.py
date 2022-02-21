import json
import re
import bcrypt
import jwt
from json.decoder import JSONDecodeError

from django.http import JsonResponse
from django.views import View
from django.db.models import Q
from django.conf import settings

from user.models import User

# META
# signup
PASSWORD_MINIMUM_LENGTH = 8
SECRET = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
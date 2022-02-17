import json
import re
from json.decoder import JSONDecodeError

from django.http import JsonResponse
from django.views import View
from django.db.models import Q

from user.models import User


PASSWORD_MINIMUM_LENGTH = 8
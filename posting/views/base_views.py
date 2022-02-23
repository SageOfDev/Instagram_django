import json
from json import JSONDecodeError

from django.http import JsonResponse
from django.views import View

from user.utils import login_decorator
from user.models import User
from posting.models import Posting
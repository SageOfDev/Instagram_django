import jwt

from django.http import JsonResponse

from .models import User
from .views.base_views import SECRET, ALGORITHM


def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_toekn = request.header.get("Authorization", None)
            payload = jwt.decode(access_toekn, SECRET, algorithm=ALGORITHM)
            request.user = User.objects.get(id=payload["id"])

        except jwt.DecodeError:
            return JsonResponse({"message": "INVALID_TOKEN"}, status=401)

        except User.DoesNotExist:
            return JsonResponse({"message": "USER_DOES_NOT_EXIST"}, status=404)

        return func(self, request, *args, **kwargs)

    return wrapper

'''
 access_token = jwt.encode({"id": user.id}, SECRET, algorithm=ALGORITHM)

        # OK:성공
        return JsonResponse({"message": "OK", "Authorization": access_token}, status=200)
'''
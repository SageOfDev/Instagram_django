from .base_views import *

class SignUpView(View):

    def post(self, request):
        try:
            data = json.loads(request.body)

            email = data.get("email", None)
            mobile_number = data.get("mobile_numer", None)
            full_name = data.get("full_name", None)
            username = data.get("username", None)
            password = data.get("password", None)

            email_pattern = re.compile(r"^.+[@].+[.].+$")
            mobile_number_pattern = re.compile(r"^[0-9]{11}$")
            username_pattern = re.compile(r"^(?=.*[a-z])[a-z0-9_.]+$")

            # KEY ERROR: 필수 입력 누락
            if not (
                    (email or mobile_number)
                and full_name
                and username
                and password
            ):
                return JsonResponse({"message": "KEY_ERROR"}, status=400)

            # VALIDATION_ERROR: 패턴과 안맞는 경우
            if email:
                if not email_pattern.match(email):
                    return JsonResponse({"message": "EMAIL_VALIDATION_ERROR"}, status=400)
            elif mobile_number:
                if not mobile_number_pattern.match(mobile_number):
                    return JsonResponse({"message": "MOBILE_NUMBER_VALIDATION_ERROR"}, status=400)
            if not username_pattern.match(username):
                return JsonResponse({"message": "USERNAME_VALIDATION_ERROR"}, status=400)
            if len(password) < PASSWORD_MINIMUM_LENGTH:
                return JsonResponse({"message": "PASSWORD_VALIDATION_ERROR"}, status=400)

            # ALREADY_EXISTS: 중복 발생
            if User.objects.filter(
                Q(email=data.get('email', 1)) |
                Q(mobile_number=data.get("mobile_number", 1)) |
                Q(username=username)
            ).exists():
                return JsonResponse({"message": "ALREADY_EXISTS"}, status=409)

            # CREATE
            User.objects.create(
                email=email,
                mobile_number=mobile_number,
                full_name=full_name,
                username=username,
                password=password
            )
            return JsonResponse({"message": "CREATE"}, status=201)

        except JSONDecodeError:
            return JsonResponse({"message": "JSON_DECODE_ERROR"}, status=400)
from .base_views import *


class LogInView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            login_id = data.get("login_id", None)
            password = data.get("password", None)

            # KEY ERROR: 필수 정보 누락
            if not (login_id and password):
                return JsonResponse({"message": "KEY_ERROR"}, status=400)

            # INVALID_ERROR
            # ID가 존재하지 않는 경우
            if not User.objects.filter(
                    Q(email=login_id) |
                    Q(mobile_number=login_id) |
                    Q(username=login_id)
            ).exists():
                return JsonResponse({"message": "INVALID_ERROR"}, status=401)
            # 비밀번호가 틀린 경우
            user = User.objects.get(
                Q(email=login_id) |
                Q(mobile_number=login_id) |
                Q(username=login_id)
            )
            if password != user.password:
                return JsonResponse({"message": "INVALID_ERROR"}, status=401)

            # SUCCESS:성공
            return JsonResponse({"message": "SECCESS"}, status=200)

        except JSONDecodeError:
            return JsonResponse({"message: JSONDecodeError"}, status=400)

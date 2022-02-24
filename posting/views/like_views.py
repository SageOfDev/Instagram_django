from .base_views import *

from posting.models import Like


class LikeView(View):
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)

            user = request.user
            posting_id = data.get("posting_id", None)

            # KEY_ERROR
            if posting_id is None:
                return JsonResponse({"message": "KEY_ERROR"}, status=400)

            # DOES_NOT_EXIST
            try:
                posting = Posting.objects.filter(id=posting_id)
            except Posting.DoesNotExist:
                return JsonResponse({"message": "POSTING_DOES_NOT_EXIST"}, status=404)

            if Like.objects.filter(user_id=user.id, posting_id=posting_id).exstis():
                Like.objects.filter(user_id=user.id, posting_id=posting_id).delete()
                like_count = Like.objects.filter(posting_id=posting_id).count()
                return JsonResponse({"message": "DELETE", 'like_count': like_count}, status=200)

            Like.objects.create(
                posting=posting,
                user=user,
            )
            like_count = Like.objects.filter(posting_id=posting_id).count()
            return JsonResponse({"message": "CREATED", "like_count": like_count}, status=201)

        except JSONDecodeError:
            return JsonResponse({"message": "JSON_DECODE_ERROR"}, status=400)
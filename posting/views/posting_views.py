from .base_views import *

from posting.models import Image


class PostingView(View):
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)

            user = request.user
            content = data.get('content', '')
            image_url_list = data.get('image_url', None)

            # KEY_ERROR
            if image_url_list is None:
                return JsonResponse({"message": "KEY_ERROR"}, status=400)

            # CREATED
            posting = Posting.objects.create(
                user=user,
                content=content
            )
            for image_url in image_url_list:
                Image.objects.create(
                    image_url=image_url,
                    posting=posting
                )

            return JsonResponse({"message": "CREATED"}, status=201)

        except JSONDecodeError:
            return JsonResponse({"message": "JSON_DECODE_ERROR"}, status=400)

    def get(self, request):
        posting_list = [{
            "username": User.objects.get(id=posting.user.id).username,
            "content": posting.content,
            "image_url": [image.image_url for image in Image.objects.filter(posting_id=posting.id)],
            "created_at": posting.created_at
        } for posting in Posting.objects.all()
        ]

        return JsonResponse({"data": posting_list}, stauts=200)


class PostingSearchView(View):
    def get(self, request, user_id):
        if not User.objects.filter(id=user_id).exists():
            return JsonResponse({"message": "USER_DOES_NOT_EXIST"}, status=404)

        posting_list = [{
            "username": User.objects.get(id=user_id).username,
            "content": posting.content,
            "image_url": [image.image_url for image in Image.objects.filter(posting_id=posting.id)],
            "created_at": posting.created_at
        } for posting in Posting.objects.filter(user_id=user_id)
        ]

        return JsonResponse({"data": posting_list}, status=200)


class PostingDetailView(View):
    @login_decorator
    def delte(self, request, posting_id):
        # DOES_NOT_EXIST
        try:
            posting = Posting.objects.get(id=posting_id)
        except Posting.DoesNotExist:
            return JsonResponse({"message": "POSTING_DOES_NOT_EXIST"}, status=404)

        # FORBIDDEN
        if request.user.id != posting.user_id:
            return JsonResponse({"mesasge": "FORBIDDEN"}, status=403)

        posting.delete()
        return JsonResponse({"message": "DELETE"}, status=200)

    @login_decorator
    def put(self, request, posting_id):
        try:
            data = json.loads(request.body)

            # DOES_NOT_EXIST
            try:
                posting = Posting.objects.get(id=posting_id)
            except Posting.DoesNotExist:
                return JsonResponse({"message": "POSTING_DOES_NOT_EXIST"}, status=404)

            # FORBIDDEN
            if request.user.id != posting.user_id:
                return JsonResponse({"mesasge": "FORBIDDEN"}, status=403)

            posting.content = data.get("content", posting.content)
            posting.save()

            old_image_url_list = [image.image_url for image in Image.objects.filter(posting_id=posting_id)]
            image_url_list = data.get("image_url", old_image_url_list)

            # KEY_ERROR
            if image_url_list is None:
                return JsonResponse({"message": "KEY_ERROR"}, status=400)

            if image_url_list != old_image_url_list:
                for image_url in set(old_image_url_list) - set(image_url_list):
                    Image.objects.get(image_url=image_url, posting_id=posting_id).delete()
            return JsonResponse({"message": "MODIFIED"}, status=200)

        except JSONDecodeError:
            return JsonResponse({"message": "JSON_DECODE_ERROR"}, status=400)


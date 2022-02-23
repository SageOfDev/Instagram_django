import json
from json.decoder import JSONDecodeError

from django.http import JsonResponse
from django.views import View

from .models import Posting, Image
from user.models import User


class PostingView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            user = User.objects.get(username=data.get('user', None))
            content = data.get('content', '')
            image_url_list = data.get('image_url', None)

            # KEYERROR
            if (user and image_url_list) is None:
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
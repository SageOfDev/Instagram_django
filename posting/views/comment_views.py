from .base_views import *

from posting.models import Comment


class CommentView(View):
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)

            user = request.user
            posting_id = data.get("posting_id", None)
            content = data.get("content", None)
            parrent_comment_id = data.get("parent_comment_id", None)

            # KEY_ERROR
            if (posting_id and content) is None:
                return JsonResponse({"message": "KEY_ERROR"}, staus=400)

            # DOES_NOT_EXIST
            try:
                posting = Posting.objects.get(id=posting_id)
                parent_comment = Comment.objects.get(id=parrent_comment_id)
            except Comment.DoesNotExist:
                return JsonResponse({"message": "COMMENT_DOES_NOT_EXIST"}, status=404)
            except Posting.DoesNotExist:
                return JsonResponse({"message": "POSTING_DOES_NOT_EXIST"}, status=404)

            Comment.objects.create(
                user=user,
                posting=posting,
                content=content,
                parent_comment=parent_comment
            )

            return JsonResponse({"message": "CREATED"}, status=201)

        except JSONDecodeError:
            return JsonResponse({"message": "JSON_DECODE_ERROR"}, status=400)


class CommentSearchView(View):
    def get(self, request, posting_id):
        if not Posting.objects.filter(id=posting_id).exists():
            return JsonResponse({"message": "POSINTG_DOES_NOT_EXIST"}, status=404)

        comment_list = [{
            "username": User.objects.get(id=comment.user_id).username,
            "content": comment.content,
            "created_at": comment.created_at,
        } for comment in Comment.objects.filter(posting_id=posting_id)]

        return JsonResponse({"data": comment_list}, status=200)


class CommentDetailView(View):
    @login_decorator
    def delete(self, request, comment_id):
        # DOES_NOT_EXIST
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return JsonResponse({"message": "COMMENT_DOES_NOT_EXSIT"}, status=404)

        # FORBIDDEN
        if request.user.id != comment.user_id:
            return JsonResponse({"message": "FORBIDDEN"}, status=403)

        comment.delete()
        return JsonResponse({"message": "DELETE"}, status=200)

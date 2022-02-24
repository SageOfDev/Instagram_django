from django.urls import path
from posting.views import posting_views, comment_views, like_views

urlpatterns = [
    path('', posting_views.PostingView.as_view()),
    path('search/<int:user_id>', posting_views.PostingSearchView.as_view()),
    path('comment', comment_views.CommentView.as_view()),
    path('comment/search/<int:posting_id>', comment_views.CommentSearchView.as_view()),
    path('like/', like_views.LikeView.as_view()),
]

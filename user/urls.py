from django.urls import path

from user.views import login_views, signup_views

urlpatterns = [
    path('signup', signup_views.SignUpView.as_view()),
    path('login', login_views.LogInView.as_view()),
]

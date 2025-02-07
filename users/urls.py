from django.urls import path
from users.views import SignUpView, LoginView, me

urlpatterns = [
    path('signup/', SignUpView.as_view()),
    path('login/', LoginView.as_view()),
    path('me/', me),
]
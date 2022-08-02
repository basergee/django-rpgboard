from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import (IndexView, CreateUserReplyView, CreatePostView,
                    EditPostView, UserProfileView, accept_reply)


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('', IndexView.as_view(), name='signup'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('create/', CreatePostView.as_view(), name='create_post'),
    path('edit/<int:pk>', EditPostView.as_view(), name='edit_post'),
    path('reply/<int:pk>', CreateUserReplyView.as_view(), name='create_reply'),
    path('accept/<int:pk>', accept_reply, name='accept_reply'),
]

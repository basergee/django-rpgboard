from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('', IndexView.as_view(), name='signup'),
    path('', IndexView.as_view(), name='profile'),
    path('', IndexView.as_view(), name='create_post'),
    path('edit/<int:pk>', IndexView.as_view(), name='edit_post'),
    path('reply/<int:pk>', IndexView.as_view(), name='create_reply'),
]

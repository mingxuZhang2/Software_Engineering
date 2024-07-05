from django.urls import path
from . import views

from django.urls import path
from . import views
from .views import UserLoginView
from .views import SignUpView

urlpatterns = [
    path('submit/', views.submit_code, name='submit_code'),
    path('generate_test_code/', views.generate_test_code, name='generate_test_code'),
    path('auto_debug/', views.auto_debug, name='auto_debug'),
    path('login/', UserLoginView.as_view(), name='login'),  # 确保 URL 正确
    path('register/', SignUpView.as_view(), name='register'),
]

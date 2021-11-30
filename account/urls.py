from django.urls import path
from . import views

urlpatterns = [
    # path('users/', views.users),
    # path('users/<int:user_id>', views.user_detail),
    path('users/change_password/', views.change_password),
    # path('users/login/', views.login),
    path('users/login/', views.user_login),
    path('users/profile/', views.profile),
    path('users/<uuid:user_id>/', views.user_detail),
    path('users/signup/', views.add_user),
    path('users/', views.get_user),
]

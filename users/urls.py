from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from .views import FollowUserView, UnfollowUserView, check_follow_status


app_name = 'users'

urlpatterns = [
    # Регистрация нового пользователя
    path('register/', views.register, name='register'),

    # Подтверждение email после регистрации
    path('confirm/<int:user_id>/', views.confirm_email, name='confirm_email'),

    # Вход в систему (используем кастомный login_view)
    path('login/', views.login_view, name='login'),

    # Выход из системы (используем стандартный Django LogoutView)
    path('logout/', auth_views.LogoutView.as_view(next_page='users:login'), name='logout'),

    # Профиль пользователя
    path('profile/', views.profile, name='profile'),

    # Редактирование профиля (новый маршрут)
    path('edit_profile/', views.edit_profile, name='edit_profile'),

    # Подписка и отписка от пользователей
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow_user'),
    path('unfollow/<int:user_id>/',
         UnfollowUserView.as_view(), name='unfollow_user'),

    path('check_follow_status/<int:user_id>/', check_follow_status, name='check_follow_status'),

    # Страница ожидания подтверждения email
    path('registration_pending/', TemplateView.as_view(
        template_name='users/registration_pending.html'), name='registration_pending'),
]

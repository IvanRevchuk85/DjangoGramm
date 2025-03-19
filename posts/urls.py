from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    # Основные маршруты постов
    path('', views.post_list, name='post_list'),  # Лента постов
    path('create/', views.create_post, name='create_post'),  # Создание поста
    path('<int:post_id>/', views.post_detail,
         name='post_detail'),  # Детальный просмотр поста

    # Действия с постом
    path('<int:post_id>/edit/', views.edit_post,
         name='edit_post'),  # Редактирование поста
    path('<int:post_id>/delete/', views.delete_post,
         name='delete_post'),  # Удаление поста

    # Лайки (используем `ManyToManyField`)
    path('<int:post_id>/like/', views.toggle_like,
         name='toggle_like'),  # Поставить/убрать лайк
]

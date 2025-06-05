from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    # Main post routes
    path('', views.post_list, name='post_list'),  # Post feed
    path('create/', views.create_post, name='create_post'),  # Create a post
    path('<int:post_id>/', views.post_detail,
         name='post_detail'),  # View post in detail

    # Actions with the post
    path('<int:post_id>/edit/', views.edit_post,
         name='edit_post'),  # Editing a post
    path('<int:post_id>/delete/', views.delete_post,
         name='delete_post'),  # Deleting post

    # Likes (using `ManyToManyField`)
    path('<int:post_id>/like/', views.toggle_like,
         name='toggle_like'),  # Like/unlike
]

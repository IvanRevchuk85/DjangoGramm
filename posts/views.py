import logging

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt  # Для тестов
from .models import Post, PostImage, Tag
from .forms import PostForm


logger = logging.getLogger(__name__)


def post_list(request):
    """Displaying a list of all posts"""
    logger.info("📌 Получен запрос на страницу постов")

    posts = Post.objects.prefetch_related(
        'images', 'likes').order_by('-created_at')

    # Checking if a post has images
    for post in posts:
        post.has_images = post.images.exists()  # Checking if a post has images

        # ✅ Add the `is_followed` attribute to check if the current user is followed
        post.is_followed = post.user.followers.filter(
            follower=request.user).exists()

    return render(request, 'posts/post_list.html', {'posts': posts})


def post_detail(request, post_id):
    """Displaying a single post with its images and tags"""
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'posts/post_detail.html', {'post': post})


@login_required
def create_post(request):
    """Create a new post with images and tags"""
    if request.method == 'POST':
        print("📌 DEBUG: Получен POST-запрос")
        # Checking if files are arriving
        print("📌 DEBUG: request.FILES ->", request.FILES)

        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()

            # Handling multiple image uploads
            images = request.FILES.getlist('images')
            if images:
                for image in images:
                    print(f"📌 DEBUG: Загружаем {image}")
                    PostImage.objects.create(post=post, image=image)

            messages.success(request, "Пост успешно создан!")
            return redirect('posts:post_list')
        else:
            print("❌ DEBUG: Форма НЕ валидна!", form.errors)
    else:
        form = PostForm()

    return render(request, 'posts/create_post.html', {'form': form})


@login_required
def edit_post(request, post_id):
    """Editing an existing post"""
    post = get_object_or_404(Post, id=post_id, user=request.user)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()

            # Updating tags
            post.tags.clear()
            tags_input = request.POST.get('tags', '')
            if tags_input:
                tag_names = [t.strip() for t in tags_input.split(',')]
                for tag_name in tag_names:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    post.tags.add(tag)

            messages.success(request, "Пост успешно обновлен!")
            return redirect('posts:post_detail', post_id=post.id)

    else:
        form = PostForm(instance=post)

    return render(request, 'posts/edit_post.html', {'form': form, 'post': post})


@login_required
def delete_post(request, post_id):
    """Deleting a post (only the author can delete their post)"""
    if request.method == "POST":
        post = get_object_or_404(Post, id=post_id, user=request.user)
        post.images.all().delete()
        post.delete()
        messages.success(request, "Пост удален.")

    return redirect('posts:post_list')


@csrf_exempt  # Remove it after fixing CSRF token transmission!
@login_required
def toggle_like(request, post_id):
    """Adding or removing a like to a post"""
    post = get_object_or_404(Post, id=post_id)

    post = get_object_or_404(Post, id=post_id)

    if request.user in post.likes.all():
        post.likes.remove(request.user)  # Delete the like
        liked = False
    else:
        post.likes.add(request.user)  # Add a like
        liked = True

    return JsonResponse({'liked': liked, 'total_likes': post.likes.count()})

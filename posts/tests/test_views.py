import pytest
from django.urls import reverse
from posts.models import Post


@pytest.mark.django_db
def test_post_list(client):
    """Тест на отображение списка постов"""
    response = client.get(reverse("posts:post_list"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_post_detail(client, test_user, test_post):
    """Тест на отображение деталей поста без HTML-шаблона"""
    response = client.get(reverse("posts:post_detail", args=[test_post.id]))

    assert response.status_code == 200
    assert test_post.content in response.content.decode()


@pytest.mark.django_db
def test_create_post(client, test_user):
    """Тест на создание нового поста"""
    client.force_login(test_user)
    response = client.post(reverse("posts:create_post"),
                           {"content": "New Post"})
    assert response.status_code == 302
    assert Post.objects.filter(content="New Post").exists()


@pytest.mark.django_db
def test_edit_post(client, test_user, test_post):
    """Тест на редактирование поста"""
    client.force_login(test_user)
    response = client.post(reverse("posts:edit_post", args=[test_post.id]), {
                           "content": "Updated Content"})
    assert response.status_code == 302
    test_post.refresh_from_db()
    assert test_post.content == "Updated Content"


@pytest.mark.django_db
def test_delete_post(client, test_user, test_post):
    """Тест на удаление поста"""
    client.force_login(test_user)
    response = client.post(reverse("posts:delete_post", args=[test_post.id]))
    assert response.status_code == 302
    assert not Post.objects.filter(id=test_post.id).exists()


@pytest.mark.django_db
def test_toggle_like(client, test_user, test_post):
    """Тест на добавление/удаление лайка"""
    client.force_login(test_user)
    response = client.post(reverse("posts:toggle_like", args=[test_post.id]))
    assert response.status_code == 200
    test_post.refresh_from_db()
    assert test_user in test_post.likes.all()

    # Удаление лайка
    response = client.post(reverse("posts:toggle_like", args=[test_post.id]))
    assert response.status_code == 200
    test_post.refresh_from_db()
    assert test_user not in test_post.likes.all()

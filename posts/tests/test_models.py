import tempfile
import os
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from posts.models import Post, PostImage, Tag
from django.core.exceptions import ValidationError
import pytest
import cloudinary.exceptions


@pytest.mark.django_db
def test_create_post(test_user):
    """Тестирует создание нового поста и проверяет его данные."""
    post = Post.objects.create(user=test_user, content="This is a test post")
    assert post.user == test_user
    assert post.content == "This is a test post"
    assert post.created_at is not None
    assert post.updated_at is not None


@pytest.mark.django_db
def test_create_tag():
    """Тестирует создание тега и проверяет его имя."""
    tag = Tag.objects.create(name="Django")
    assert tag.name == "Django"


@pytest.mark.django_db
def test_create_post_image(test_user):
    """Тестирует загрузку изображения в пост и проверяет его сохранение."""
    post = Post.objects.create(user=test_user, content="Test Post")

    temp_image = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
    image = Image.new("RGB", (100, 100), color="red")
    image.save(temp_image, format="JPEG")
    temp_image.seek(0)

    uploaded_image = SimpleUploadedFile(
        temp_image.name, temp_image.read(), content_type="image/jpeg")
    post_image = PostImage.objects.create(post=post, image=uploaded_image)
    assert post_image.post == post
    assert post_image.image is not None

    temp_image.close()
    os.unlink(temp_image.name)


@pytest.mark.django_db
def test_image_validation(test_user):
    """Тестирует валидацию загружаемого файла (ошибка, если файл не изображение)."""
    post = Post.objects.create(user=test_user, content="Invalid Image Test")
    invalid_file = SimpleUploadedFile(
        "test.txt", b"this is not an image", content_type="text/plain")

    post_image = PostImage(post=post, image=invalid_file)

    with pytest.raises(cloudinary.exceptions.Error, match="Invalid image file"):
        post_image.full_clean()  # Проверяем валидацию перед сохранением
        post_image.save()


@pytest.mark.django_db
def test_delete_post_cascade(test_user):
    """Тест на каскадное удаление поста (должны удалиться связанные изображения и теги)."""
    post = Post.objects.create(user=test_user, content="Post for deletion")
    tag = Tag.objects.create(name="TestTag")
    tag.save()
    post.tags.add(tag)

    temp_image = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
    image = Image.new("RGB", (100, 100), color="red")
    image.save(temp_image, format="JPEG")
    temp_image.seek(0)

    uploaded_image = SimpleUploadedFile(
        temp_image.name, temp_image.read(), content_type="image/jpeg"
    )
    post_id = post.id

    post_image = PostImage.objects.create(post=post, image=uploaded_image)

    post.delete()

    assert not Post.objects.filter(id=post.id).exists()
    assert not PostImage.objects.filter(post_id=post_id).exists()

    tag.refresh_from_db()
    assert tag.posts.count() == 0

    temp_image.close()
    os.unlink(temp_image.name)

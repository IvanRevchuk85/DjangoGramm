import pytest
import tempfile
import os
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from posts.forms import PostForm


@pytest.mark.django_db
def test_valid_post_form():
    """Тест на успешное создание поста через форму."""
    form_data = {
        "content": "This is a test post.",
        "tags": "django, python, testing"
    }
    form = PostForm(data=form_data)
    assert form.is_valid(), form.errors
    assert form.cleaned_data["tags"] == "django, python, testing"


@pytest.mark.django_db
def test_post_form_empty_content():
    """Тест, что форма позволяет пустое поле content."""
    form_data = {"content": "", "tags": "test, tag"}
    form = PostForm(data=form_data)
    assert form.is_valid(), form.errors


@pytest.mark.django_db
def test_post_form_tag_processing():
    """Тест обработки тегов (удаление пробелов, корректное форматирование)."""
    form_data = {
        "content": "This is another test post.",
        "tags": "  tag1 , tag2 ,  tag3  , "
    }
    form = PostForm(data=form_data)
    assert form.is_valid(), form.errors
    assert form.cleaned_data["tags"] == "tag1, tag2, tag3"


@pytest.mark.django_db
def test_post_form_with_image():
    """Тест создания поста с изображением."""
    temp_image = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
    image = Image.new("RGB", (100, 100), color="blue")
    image.save(temp_image, format="JPEG")
    temp_image.seek(0)

    uploaded_image = SimpleUploadedFile(
        temp_image.name, temp_image.read(), content_type="image/jpeg"
    )

    form_data = {
        "content": "Post with image",
        "tags": "photo, test"
    }
    form = PostForm(data=form_data, files={"image": uploaded_image})

    assert form.is_valid(), form.errors
    assert form.cleaned_data["tags"] == "photo, test"

    temp_image.close()
    os.unlink(temp_image.name)


@pytest.mark.django_db
def test_post_form_without_image():
    """Тест на успешное создание поста без изображения."""
    form_data = {
        "content": "Post without image",
        "tags": "tag1, tag2"
    }
    form = PostForm(data=form_data)
    assert form.is_valid(), form.errors


@pytest.mark.django_db
def test_post_form_without_content():
    """Тест на успешное создание поста без текста (только изображение)."""
    form_data = {
        "content": "",
        "tags": "tag1, tag2"
    }
    form = PostForm(data=form_data)

    assert form.is_valid(), form.errors


@pytest.mark.django_db
def test_post_form_invalid_tags():
    """Тест на обработку невалидных тегов (пустые, спецсимволы)."""
    form_data = {
        "content": "Post with bad tags",
        "tags": "!!, ##, $$, python "
    }
    form = PostForm(data=form_data)
    assert form.is_valid(), form.errors
    assert form.cleaned_data["tags"] == "!!, ##, $$, python"


@pytest.mark.django_db
def test_post_form_max_length_content():
    """Тест на максимальную длину контента."""
    form_data = {
        "content": "A" * 5000,  # Предположим, что макс. длина 5000
        "tags": "long, test"
    }
    form = PostForm(data=form_data)
    assert form.is_valid(), form.errors

from django import forms
from .models import Post
from cloudinary.models import CloudinaryField


class PostForm(forms.ModelForm):
    """
    Форма для создания и редактирования постов.
    Поле 'content' - текст поста.
    Поле 'tags' - ввод тегов через запятую.
    """
    tags = forms.CharField(
        max_length=255,
        required=False,
        help_text="Введите теги через запятую"
    )

    class Meta:
        model = Post
        fields = ['content', 'tags', 'image']

    def clean_tags(self):
        """
        Очистка и обработка списка тегов.
        Убираем пробелы, пустые значения.
        """
        tags = self.cleaned_data.get('tags', '')
        tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
        return ', '.join(tag_list)

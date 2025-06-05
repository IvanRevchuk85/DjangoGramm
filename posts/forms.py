from django import forms
from .models import Post
from cloudinary.models import CloudinaryField


class PostForm(forms.ModelForm):
    """
    Form for creating and editing posts.
    Field 'content' - post text.
    Field 'tags' - enter tags separated by commas.
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
        Cleaning and processing the list of tags.
        Removing spaces, empty values.
        """
        tags = self.cleaned_data.get('tags', '')
        tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
        return ', '.join(tag_list)

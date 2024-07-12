from django import forms
from .models import Post, Tag


class PostForm(forms.ModelForm):
    tags = forms.CharField(required=False, help_text="Comma-separated tags")
    author_name = forms.CharField(required=False, help_text="Your name (optional)")

    class Meta:
        model = Post
        fields = ["title", "content"]

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            tag_names = [
                name.strip()
                for name in self.cleaned_data["tags"].split(",")
                if name.strip()
            ]

            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(name=tag_name.lower())
                instance.tags.add(tag)
        return instance
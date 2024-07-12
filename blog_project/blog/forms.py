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
        author_name = self.cleaned_data.get("author_name")
        if not author_name:
            author_name = "Anonymous"

        instance.author = author_name

        if commit:
            instance.save()
            self.save_tags(instance)

        return instance

    def save_tags(self, instance):
        tag_names = [
            name.strip()
            for name in self.cleaned_data["tags"].split(",")
            if name.strip()
        ]
        instance.tags.clear()  # Remove existing tags
        for tag_name in tag_names:
            tag, created = Tag.objects.get_or_create(name=tag_name.lower())
            instance.tags.add(tag)

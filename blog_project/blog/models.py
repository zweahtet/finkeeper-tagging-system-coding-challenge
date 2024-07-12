from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    content = models.TextField()
    author = models.CharField(max_length=100, db_index=True)
    date = models.DateTimeField(auto_now_add=True, db_index=True)
    tags = models.ManyToManyField("Tag", related_name="posts")

    def __str__(self):
        return self.title
    
    class Meta:
        indexes = [
            models.Index(fields=["title", "author"]), # Composite index for title and author
            models.Index(fields=["date", "author"]), # Composite index for date and author
        ]


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, db_index=True)

    def __str__(self):
        return self.name

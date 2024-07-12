from django.core.management.base import BaseCommand
from django.utils import timezone
from blog.models import Post, Tag
import random
import lorem


class Command(BaseCommand):
    help = "Generates 100 dummy blog posts with random tags"

    def handle(self, *args, **kwargs):
        # Create some sample tags
        tags = [
            "Technology",
            "Programming",
            "Python",
            "Django",
            "Web Development",
            "Data Science",
            "Machine Learning",
            "AI",
            "Cloud Computing",
            "DevOps",
            "Cybersecurity",
            "Blockchain",
            "IoT",
            "Mobile Development",
            "Frontend",
            "Backend",
            "Database",
            "API",
            "Networking",
            "Linux",
        ]

        for tag_name in tags:
            Tag.objects.get_or_create(name=tag_name)

        # Generate 100 dummy posts
        for i in range(100):
            title = f"Blog Post {i+1}: {lorem.sentence()[:50]}"
            content = lorem.paragraph()
            author = f"Author {random.randint(1, 10)}"
            date = timezone.now() - timezone.timedelta(days=random.randint(0, 365))

            post = Post.objects.create(
                title=title, content=content, author=author, date=date
            )

            # Add random tags to the post
            num_tags = random.randint(1, 5)
            random_tags = random.sample(tags, num_tags)
            for tag_name in random_tags:
                tag = Tag.objects.get(name=tag_name)
                post.tags.add(tag)

            self.stdout.write(self.style.SUCCESS(f"Created post: {title}"))

        self.stdout.write(
            self.style.SUCCESS("Successfully generated 100 dummy blog posts")
        )

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Post, Tag


class TaggingSystemTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.post = Post.objects.create(
            title="Test Post", content="Content", author=self.user
        )

    def test_tag_creation(self):
        tag = Tag.objects.create(name="testtag")
        self.assertEqual(tag.name, "testtag")

    def test_tag_association(self):
        tag = Tag.objects.create(name="testtag")
        self.post.tags.add(tag)
        self.assertIn(tag, self.post.tags.all())

    def test_tag_search(self):
        tag1 = Tag.objects.create(name="tag1")
        tag2 = Tag.objects.create(name="tag2")
        self.post.tags.add(tag1, tag2)

        response = self.client.get(
            reverse("search_posts") + "?q=tag1,tag2&filter_type=all"
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)

        response = self.client.get(reverse("search_posts") + "?q=tag1&filter_type=any")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)

    def test_tag_uniqueness(self):
        Tag.objects.create(name="unique")
        with self.assertRaises(Exception):
            Tag.objects.create(name="unique")

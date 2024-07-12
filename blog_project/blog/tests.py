from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Post, Tag


class TaggingSystemTests(TestCase):
    def setUp(self):
        self.post = Post.objects.create(
            title="Test Post", content="Test Content", author="Test Author"
        )
        self.tag1 = Tag.objects.create(name="tag1")
        self.tag2 = Tag.objects.create(name="tag2")
        self.post.tags.add(self.tag1, self.tag2)

    def test_tag_creation(self):
        tag = Tag.objects.create(name="newtag")
        self.assertEqual(Tag.objects.count(), 3)

    def test_tag_association(self):
        self.assertEqual(self.post.tags.count(), 2)

    def test_search_by_tag(self):
        response = self.client.get(reverse("search_posts") + "?q=tag1&filter_type=any")
        self.assertContains(response, "Test Post")

    def test_filter_all_tags(self):
        response = self.client.get(
            reverse("search_posts") + "?q=tag1,tag2&filter_type=all"
        )
        self.assertContains(response, "Test Post")

    def test_filter_any_tags(self):
        response = self.client.get(
            reverse("search_posts") + "?q=tag1,nonexistent&filter_type=any"
        )
        self.assertContains(response, "Test Post")

    def test_filter_specific_combination(self):
        response = self.client.get(
            reverse("search_posts") + "?q=tag1,tag2&filter_type=specific"
        )
        self.assertContains(response, "Test Post")

    def test_popular_tags(self):
        response = self.client.get(reverse("search_posts"))
        self.assertContains(response, "tag1")
        self.assertContains(response, "tag2")

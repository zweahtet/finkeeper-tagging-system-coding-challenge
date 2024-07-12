from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.create_post, name="create_post"),
    path("post/<int:post_id>/manage-tags/", views.manage_tags, name="manage_tags"),
    path("search/", views.search_posts, name="search_posts"),
]
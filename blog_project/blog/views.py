from django.shortcuts import render, redirect
from django.core.cache import cache
from django.db.models import Count
from .models import Post, Tag
from .forms import PostForm

def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            author_name = form.cleaned_data.get("author_name", "Anonymous")
            post.author = author_name
            post.save()
            form.save_m2m()  # Save the tags
            cache.delete("all_tags")  # Invalidate the all_tags cache
            cache.delete("popular_tags")  # Invalidate the popular_tags cache
            return redirect("search_posts")
    else:
        form = PostForm()
    return render(request, "blog/create_post.html", {"form": form})


def manage_tags(request, post_id):
    post = Post.objects.get(pk=post_id)
    if request.method == "POST":
        tag_names = request.POST.get("tags", "").split(",")
        post.tags.clear()
        for tag_name in tag_names:
            tag, created = Tag.objects.get_or_create(name=tag_name.strip().lower())
            post.tags.add(tag)
        cache.delete("all_tags")  # Invalidate the all_tags cache
        cache.delete("popular_tags")  # Invalidate the popular_tags cache
        return redirect("search_posts")
    return render(request, "blog/manage_tags.html", {"post": post})


def get_all_tags():
    tags = cache.get("all_tags")
    if tags is None:
        tags = list(Tag.objects.all())
        cache.set("all_tags", tags, timeout=3600)  # Cache for 1 hour
    return tags


def get_popular_tags(limit=10):
    popular_tags = cache.get("popular_tags")
    if popular_tags is None:
        popular_tags = Tag.objects.annotate(post_count=Count("posts")).order_by(
            "-post_count"
        )[:limit]
        cache.set("popular_tags", popular_tags, timeout=3600)  # Cache for 1 hour
    return popular_tags

def search_posts(request):
    query = request.GET.get("q", "")
    filter_type = request.GET.get("filter_type", "any")
    tags = [tag.strip() for tag in query.split(",")] if query else []

    cache_key = f"search_results_{query}_{filter_type}"
    posts = cache.get(cache_key)

    if posts is None:
        if tags:
            if filter_type == "all":
                posts = Post.objects.filter(tags__name__in=tags).distinct()
                for tag in tags:
                    posts = posts.filter(tags__name=tag)
            elif filter_type == "any":
                posts = Post.objects.filter(tags__name__in=tags).distinct()
            elif filter_type == "specific":
                posts = Post.objects.filter(tags__name__in=tags)
                posts = posts.annotate(tag_count=Count("tags")).filter(
                    tag_count=len(tags)
                )
            else:
                posts = Post.objects.all()
        else:
            posts = Post.objects.all()

        posts = list(posts)
        cache.set(cache_key, posts, timeout=300)  # Cache for 1 hour

    all_tags = get_all_tags()
    popular_tags = get_popular_tags()

    return render(
        request,
        "blog/search_results.html",
        {
            "posts": posts,
            "query": query,
            "filter_type": filter_type,
            "all_tags": all_tags,
            "popular_tags": popular_tags,
        },
    )

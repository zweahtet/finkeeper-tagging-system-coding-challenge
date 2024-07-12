from django.shortcuts import render, redirect
from django.contrib.auth.models import User
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
            # Redirect to search results page
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
        return redirect("search_posts")
    return render(request, "blog/manage_tags.html", {"post": post})


def search_posts(request):
    query = request.GET.get("q", "")
    filter_type = request.GET.get("filter_type", "any")
    tags = [tag.strip() for tag in query.split(",")] if query else []

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            author_name = form.cleaned_data["author_name"]
            if request.user.is_authenticated:
                post.author = request.user
            elif author_name:
                user, created = User.objects.get_or_create(username=author_name)
                post.author = user
            post.save()
            form.save_m2m()  # Save the tags
            return redirect("search_posts")
    else:
        form = PostForm()

    if tags:
        if filter_type == "all":
            posts = Post.objects.filter(tags__name__in=tags).distinct()
            for tag in tags:
                posts = posts.filter(tags__name=tag)
        elif filter_type == "any":
            posts = Post.objects.filter(tags__name__in=tags).distinct()
        elif filter_type == "specific":
            posts = Post.objects.filter(tags__name__in=tags)
            posts = posts.annotate(tag_count=Count("tags")).filter(tag_count=len(tags))
        else:
            posts = Post.objects.all()
    else:
        posts = Post.objects.all()

    context = {"posts": posts, "query": query, "filter_type": filter_type, "form": form}
    return render(request, "blog/search_results.html", context)

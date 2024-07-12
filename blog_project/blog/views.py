from django.shortcuts import render, redirect
from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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
    page = request.GET.get("page", 1)

    cache_key = f"search_results_{query}_{filter_type}_{page}"
    cached_result = cache.get(cache_key)

    if cached_result is None:
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

        # Order posts by date (newest first)
        posts = posts.order_by("-date")

        # Pagination
        paginator = Paginator(posts, 10)  # Show 10 posts per page
        try:
            paginated_posts = paginator.page(page)
        except PageNotAnInteger:
            paginated_posts = paginator.page(1)
        except EmptyPage:
            paginated_posts = paginator.page(paginator.num_pages)

        cached_result = {
            "posts": list(paginated_posts),
            "has_previous": paginated_posts.has_previous(),
            "has_next": paginated_posts.has_next(),
            "previous_page_number": (
                paginated_posts.previous_page_number()
                if paginated_posts.has_previous()
                else None
            ),
            "next_page_number": (
                paginated_posts.next_page_number()
                if paginated_posts.has_next()
                else None
            ),
            "current_page": paginated_posts.number,
            "total_pages": paginator.num_pages,
        }
        cache.set(cache_key, cached_result, 300)  # Cache for 5 minutes

    all_tags = get_all_tags()
    popular_tags = get_popular_tags()

    return render(
        request,
        "blog/search_results.html",
        {
            "posts": cached_result["posts"],
            "query": query,
            "filter_type": filter_type,
            "all_tags": all_tags,
            "popular_tags": popular_tags,
            "has_previous": cached_result["has_previous"],
            "has_next": cached_result["has_next"],
            "previous_page_number": cached_result["previous_page_number"],
            "next_page_number": cached_result["next_page_number"],
            "current_page": cached_result["current_page"],
            "total_pages": cached_result["total_pages"],
        },
    )

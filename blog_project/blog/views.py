from django.shortcuts import render, redirect
from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from .models import Post, Tag
from .forms import PostForm
from .utils import get_all_tags, get_popular_tags


def create_post(request):
    """
    View to handle creating a new post.

    If the request method is POST, it processes the form data, saves the post
    along with its author and tags, invalidates the relevant cache, and redirects
    to the search posts page. If the request method is GET, it renders an empty form.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object containing the rendered form or redirect.
    """
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save()

            return redirect("search_posts")
    else:
        form = PostForm()
    return render(request, "blog/create_post.html", {"form": form})


def manage_tags(request, post_id):
    """
    View to handle managing tags for a specific post.

    If the request method is POST, it updates the tags for the post, invalidates
    the relevant cache, and redirects to the search posts page. If the request method
    is GET, it renders the tag management page.

    Args:
        request (HttpRequest): The request object.
        post_id (int): The ID of the post to manage tags for.

    Returns:
        HttpResponse: The response object containing the rendered tag management page or redirect.
    """
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
    """
    View to handle searching for posts based on tags and filter type.

    This function retrieves posts based on the search query, filter type, and pagination.
    It uses caching to store and retrieve search results for efficiency.

    Args:
        request (HttpRequest): The request object containing query parameters.

    Returns:
        HttpResponse: The response object containing the rendered search results page.
    """
    query = request.GET.get("q", "")
    filter_type = request.GET.get("filter_type", "all")
    tags = [tag.strip() for tag in query.split(",")] if query else []
    page = request.GET.get("page", 1)

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

    all_tags = get_all_tags()
    popular_tags = get_popular_tags()

    return render(
        request,
        "blog/search_results.html",
        {
            "posts": paginated_posts,
            "query": query,
            "filter_type": filter_type,
            "all_tags": all_tags,
            "popular_tags": popular_tags,
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
        },
    )

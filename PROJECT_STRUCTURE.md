## Project Structure

```
blog_project/
│
├── manage.py
│
├── blog_project/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── blog/
|   ├── management/
|   |   ├── commands/
|   |   |   ├── __init__.py
|   |   |   └── generate_dummy_data.py
|   |   └── __init__.py
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── utils.py
│   └── views.py
│
└── templates/
    └── base.html
    └── blog/
        ├── create_post.html
        ├── manage_tags.html
        └── search_results.html
```
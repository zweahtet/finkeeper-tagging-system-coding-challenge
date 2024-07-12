# Blog Project

This is a Django-based blogging platform where users can create posts and add tags to categorize and organize their content. The platform includes robust tagging functionality, search, and filtering capabilities.

## Features

- Create and manage blog posts
- Add and manage tags for posts
- Search and filter posts by tags
- Admin interface for managing posts and tags

## Requirements

- Python 3.6+
- Django 3.2+
- Virtualenv (recommended)

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/zweahtet/finkeeper-tagging-system-coding-challenge.git
cd blog_project
```

### 2. Set Up a Virtual Environment

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 4. Configure the Database

The project uses SQLite by default, which requires no additional setup. If you want to use a different database, update the `DATABASES` setting in `blog_project/settings.py`.

### 5. Apply Migrations

Create and apply database migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a Superuser

Create a superuser account to access the Django admin interface:

```bash
python manage.py createsuperuser
```

### 7. Run the Development Server

Start the Django development server:

```bash
python manage.py runserver
```

Open your web browser and go to `http://127.0.0.1:8000/` to see the application in action.

## Usage

### Admin Interface

Access the admin interface at `http://127.0.0.1:8000/admin/` to manage posts and tags. Log in with the superuser credentials you created earlier.

### Creating Posts

Visit `http://127.0.0.1:8000/blog/create/` to create a new blog post. You can add tags to your post by entering comma-separated tag names.

### Managing Tags

To manage tags for a specific post, visit `http://127.0.0.1:8000/blog/post/<post_id>/manage-tags/`.

### Searching and Filtering Posts

Visit `http://127.0.0.1:8000/blog/search/` to search for posts by tags. You can filter posts by:
- All tags: Show posts that contain all specified tags.
- Any tags: Show posts that contain at least one of the specified tags.
- Specific combination of tags: Show posts that match a specific set of tags.

## Project Structure

```
blog_project/
│
├── manage.py
│
├── blog_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── blog/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   ├── tests.py
│   ├── utils.py
│   └── templates/
│       ├── create_post.html
│       ├── manage_tags.html
│       └── search_results.html
│
└── templates/
    └── base.html
```

## Running Tests

To run the tests for the blog application:

```bash
python manage.py test blog
```

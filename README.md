# Blog Tagging System

Welcome to my Blog Tagging System project! This Django-based application is the result of my efforts to create a robust and efficient tagging system for a blogging platform. As a developer, I wanted to tackle the challenge of implementing a feature-rich system that allows users to easily categorize and find content.

## Project Overview

In developing this system, I focused on creating a user-friendly experience for both content creators and readers. Here's what I've built:

- **Post Creation**: Users can create blog posts with titles, content, and multiple tags.
- **Tag Management**: I've implemented a flexible tagging system where users can add, remove, and manage tags for each post.
- **Advanced Search and Filtering**: One of the key features I'm proud of is the search functionality. Users can find posts using tag-based searches with options to filter by all tags, any tags, or specific combinations.
- **Performance Optimization**: Knowing that performance is crucial, I've incorporated database indexing and caching mechanisms to ensure quick response times, even with a large number of posts and tags.
- **Pagination**: To handle potentially large sets of search results, I've implemented pagination to improve load times and user experience.

## Technical Highlights

- **Django Framework**: I chose Django for its robustness and built-in features that align well with the project requirements.
- **Database Design**: I've designed the models to efficiently handle the many-to-many relationship between posts and tags.
- **Caching Strategy**: To optimize performance, I implemented caching for frequently accessed data like popular tags and search results.
- **Testing**: I've written comprehensive tests to ensure the reliability and correctness of the tagging and search functionalities.

## Learning Experience

This project has been an excellent opportunity for me to deepen my understanding of Django, database optimization techniques, and the implementation of search functionalities. I've particularly enjoyed solving the challenges around efficient tag-based searching and ensuring the system remains performant as the dataset grows.

I hope you find this project interesting and potentially useful for your own blogging needs. Feel free to explore the code, run the application, and let me know if you have any questions or suggestions for improvement!

## Setup and Installation
### Requirements

- Python 3.6+
- Django 3.2+
- Virtualenv (recommended)

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

### 6. Generate dummy data (Optional, but recommended)

Generate 100 dummy posts with 20 random tags for live testing:

```bash
python manage.py generate_dummy_data
```

### 7. Create a Superuser (Optional)

Create a superuser account to access the Django admin interface:

```bash
python manage.py createsuperuser
```

### 8. Run the Development Server

Start the Django development server:

```bash
python manage.py runserver
```

Open your web browser and go to `http://127.0.0.1:8000/blog/search/` to see the application in action.

## Usage

### Admin Interface

Access the admin interface at `http://127.0.0.1:8000/admin/` to manage posts and tags. Log in with the superuser credentials you created earlier.

### Creating Posts

Visit `http://127.0.0.1:8000/blog/create/` to create a new blog post. You can add tags to your post by entering comma-separated tag names.

### Searching and Filtering Posts

Visit `http://127.0.0.1:8000/blog/search/` to search for posts by tags. You can filter posts by:
- All tags: Show posts that contain all specified tags.
- Any tags: Show posts that contain at least one of the specified tags.
- Specific combination of tags: Show posts that match a specific set of tags.

## Running Tests

To run the tests for the blog application:

```bash
python manage.py test blog
```

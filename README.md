![plot](api_yamdb/static/img/yambd-high-resolution-color-logo.png)

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li>
        <a href="#usage">Usage</a>
        <ul>
            <li><a href="#available_urls">Available urls</a></li>
            <li><a href="#database_requests">Database requests</a></li>
        </ul>
    </li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>

## About The Project
This is api service, where you can get or create reviews, ratings, comments on the different content.

### Built With
* Python
* SQLite
* Django

## Getting Started

### Prerequisites
1. Clone the repo
  ```sh
  git clone ...
  ```

2. Make and activate virtual environment
  ```sh
  python -m venv venv
  ```
  ```sh
  source venv/Scripts/activate
  ```

### Installation

1. Upgrade pip, install requirements
  ```sh
  python -m pip install --upgrade pip
  ```
  ```sh
  pip install -r requirements.txt
  ```

2. Make migrations
  ```sh
  python manage.py makemigrations
  ```
  ```sh
  python manage.py migrate
  ```

3. Run server
  ```sh
  python manage.py runserver
  ```

## Usage

You may use Postman to create api requests.
Only auth users can make reviews and leave comments.
So your first goal is to **Sign Up** and then **Sign In**.

### Available urls

...

### Database requests
  
More data and examples available on ```127.0.0.1:8000/redoc/```



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
* [SQLite](https://www.sqlite.org/docs.html)
* [Django](https://django.fun/ru/docs/django/3.2/)
* [Rest-framework](https://www.django-rest-framework.org/)
* [SimpleJWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/index.html)
* [Pytest](https://docs.pytest.org/en/7.2.x/)

# Blog

A Django-powered blogging platform with social features, image sharing, real-time chat, and a REST API. The project combines a traditional blog frontend with modern async communication and containerized deployment.

## Features

- Blog posts with rich metadata, tags, comments, search, and RSS feed support
- User dashboard, registration, profiles, and follow interactions
- Image gallery with likes, rankings, and upload management
- Real-time chat rooms using Django Channels and Redis
- REST API powered by Django REST Framework and OpenAPI schema generation
- Celery background task support and Redis-based caching/channel layer
- Optional Docker deployment with PostgreSQL, Redis, Nginx, and TLS automation

## Tech Stack

- Python 3.12+
- Django 6.1+
- Django REST Framework
- django-allauth + dj-rest-auth
- Django Channels + Redis
- Celery
- PostgreSQL (or SQLite for local dev)
- Docker Compose
- Tailwind-free custom HTML/CSS templates

## Project Structure

```text
.
├── accounts/          # user auth, profile, dashboard, follow logic
├── actions/           # social actions and activity tracking
├── blog/              # posts, comments, feed, search, API
├── chat/              # WebSocket chat app
├── images/            # gallery, ranking, likes, uploads
├── mysite/            # project settings, URLs, Celery, ASGI
├── templates/         # HTML templates
├── static/            # CSS and frontend assets
├── utils/             # helper modules
├── docker-compose.yml # container orchestration
├── Dockerfile         # app container
├── manage.py          # Django entry point
├── pyproject.toml     # Python project metadata and dependencies
├── db.sqlite3         # default SQLite DB for local development
├── nginx/             # Nginx config
└── README.md          # project documentation
```

## Requirements

- Python 3.12+
- Redis
- PostgreSQL (recommended for production/container setup)
- Optional: Docker and Docker Compose

## Local Development Setup

1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -e .
```

For development tools used in the project, install the optional dev dependencies as well:

```bash
python -m pip install "django-debug-toolbar>=8.0.0" "django-redisboard>=9.0.0" "flower>=2.2.0"
```

3. Configure environment variables. Create a `.env` file in the project root with values similar to:

```env
SECRET_KEY=change-me
DEBUG=True
DB_ENGINE=sqlite
DEFAULT_FROM_EMAIL=no-reply@example.com
ADMIN_EMAIL_USERNAME=admin
ADMIN_EMAIL_ADDRESS=admin@example.com
ALLOWED_HOSTS=localhost,127.0.0.1

REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/1
```

For PostgreSQL-based local or Docker runs, use:

```env
DB_ENGINE=postgresql
DB_NAME=blog
DB_USER=blog
DB_PASSWORD=blog
DB_HOST=localhost
DB_PORT=5432
```

4. Run database migrations:

```bash
python manage.py migrate
```

5. Create an admin user:

```bash
python manage.py createsuperuser
```

6. Start the app:

```bash
python manage.py runserver
```

To run the async chat layer in a local environment that matches production behavior, use Daphne instead of the default server:

```bash
daphne -b 0.0.0.0 -p 8000 mysite.asgi:application
```

For Celery workers and Redis, run in separate terminals:

```bash
redis-server
celery -A mysite worker --loglevel=info
```

## Docker Setup

This project includes a Docker Compose configuration for running the web app, Celery worker, PostgreSQL, Redis, Nginx, and certificate automation.

```bash
docker compose up --build
```

This starts the main app stack and exposes the frontend through Nginx. The app is configured to use PostgreSQL and Redis inside the Compose network.

For HTTPS deployment, set the required environment variables in `.env`:

```env
DOMAIN=your-domain.example.com
LETSENCRYPT_EMAIL=you@example.com
```

Then initialize certificates before bringing the stack up:

```bash
docker compose run --rm --no-deps --service-ports certbot-init
docker compose up -d
```

## URLs and Entry Points

- Frontend blog: `/blog/`
- User account dashboard: `/accounts/`
- Admin panel: `/admin/`
- Image gallery: `/images/`
- Chat rooms: `/chat/room/<room_id>/`
- API schema: `/api/schema/`
- Swagger UI: `/api/schema/swagger-ui/`
- Redoc: `/api/schema/redoc/`

## API Notes

The project exposes a blog API under `/api/v1/blog/` and also includes Django REST auth endpoints under `/api/dj-rest-auth/`.

## Useful Commands

```bash
python manage.py check
python manage.py makemigrations
python manage.py migrate
python manage.py test
python manage.py collectstatic
```

## Notes

- The app uses Redis for both cache and Channels support.
- Production deployment is designed around HTTPS via Nginx and Certbot.
- The default project uses environment-based secrets and configuration instead of hard-coded settings.

## License

This project currently does not declare a license file. Add a license before publishing or distributing it publicly.

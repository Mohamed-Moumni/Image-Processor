# Image Processor

A concise Django REST API for image upload, processing, and user management, with MinIO storage and Docker Compose support.

## Features

- User authentication
- Image upload & processing
- MinIO object storage

## Quick Start

````bash
git clone <repo-url>
cd Image-Processor
docker-compose up --build
# Image Processor

A concise Django REST API for uploading, transforming, and managing images. Built with Django REST Framework, MinIO for object storage, and optional Docker Compose for local development.

## Key Features

- User authentication and management
- Image upload, storage, and server-side transformations
- MinIO-backed object storage (S3-compatible)
- Clear service separation: image, transformation, and user services

## Tech Stack

- Python, Django, Django REST Framework
- MinIO (S3-compatible object storage)
- Docker & Docker Compose (optional)

## Quick Start (Docker)

1. Clone the repo:

```bash
git clone <repo-url>
cd Image-Processor
# Image Processor

A Django REST API for uploading, processing, and managing images. Built with modular services, MinIO object storage integration, and Docker Compose for easy local development.

## Overview

This project provides simple REST endpoints for user management and image operations. Uploaded images are stored in MinIO and processed via service-layer components to keep the API thin and testable.

## Key Features

- Authentication and user management
- Image upload, listing, and download
- Image processing hooks (resize, convert, pipelines)
- MinIO-backed object storage
- Docker Compose for local development

## Quick start

```bash
git clone <repo-url>
cd Image-Processor
docker-compose up --build
````

API base: http://localhost:8000/

## API (examples)

- `POST /api/users/` — create user
- `POST /api/auth/login/` — obtain auth token
- `GET /api/images/` — list images
- `POST /api/images/` — upload image (multipart/form-data)
- `GET /api/images/<id>/` — retrieve image metadata or download

See `imgproc/api/` for exact request and response formats.

## Configuration

Copy and edit the environment template:

```bash
cp .env.template .env
# set MINIO credentials, DJANGO_SECRET_KEY, DB settings, etc.
```

Notable env vars: `MINIO_ENDPOINT`, `MINIO_ACCESS_KEY`, `MINIO_SECRET_KEY`, `DJANGO_SECRET_KEY`.

## Development notes

- Core app: `imgproc/api/` (models, serializers, services, views)
- MinIO helper: `imgproc/api/services/minio_service.py`
- Tests: `pytest` (if present) or Django test runner

## Requirements

- Docker & Docker Compose
- Python 3.8+
- See `requirements.txt` for Python dependencies

## Contributing

Contributions are welcome. Open an issue or a pull request; include tests for new behavior.

## License

MIT License

3. Run migrations and start the server:

```bash
python imgproc/manage.py migrate
python imgproc/manage.py createsuperuser  # optional
python imgproc/manage.py runserver
```

## API Overview (concise)

- POST /api/images/ — Upload an image (multipart/form-data)
- GET /api/images/{id}/ — Retrieve image metadata and URL
- POST /api/transformations/ — Request transformations (resize, crop, filters)
- GET /api/users/ — User endpoints (auth/management)

Refer to the `api/` package for detailed serializers and views.

## Running Tests

Run unit tests with:

```bash
pytest
```

## Project Structure (high level)

- `imgproc/` — Django project
- `api/` — application code (models, serializers, views, services, urls)
- `api/services/` — business logic (MinIO, transformations, users)
- `docker-compose.yml` — local dev setup with MinIO and Django

## Contributing

1. Fork the repo and create a feature branch
2. Run tests and linters locally
3. Open a PR with a clear description of changes

## Troubleshooting & Notes

- If using Docker Compose, ensure MinIO ports (9000) are free.
- Check environment variables for MinIO credentials if uploads fail.

---

If you'd like, I can add a short example curl request for uploading an image or link a Swagger/OpenAPI spec — tell me which you prefer.

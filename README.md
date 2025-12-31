# Image Processor

A Django-based RESTful API for image processing and management, featuring user authentication and MinIO integration for object storage. The project is containerized using Docker Compose for easy deployment.

## Features

- User registration and authentication
- Image upload, retrieval, and management
- Image processing services
- MinIO integration for scalable object storage
- Modular Django app structure
- API endpoints for user and image operations

## Project Structure

- `imgproc/` — Django project root
  - `api/` — Main app with models, serializers, services, views, and URLs
  - `imgproc/` — Django settings and configuration
- `docker-compose.yml` — Multi-container orchestration
- `requirements.txt` — Python dependencies

## Getting Started

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd Image-Processor
   ```
2. **Start services with Docker Compose:**
   ```bash
   docker-compose up --build
   ```
3. **Access the API:**
   - Default: `http://localhost:8000/`

## API Overview

- `/api/users/` — User registration & authentication
- `/api/images/` — Image upload & management

## Requirements

- Docker & Docker Compose
- Python 3.8+

## License

MIT License

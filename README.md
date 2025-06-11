# django-chatbot-rag

A Django-based Retrieval-Augmented Generation (RAG) chatbot application that provides intelligent, context-aware conversations.

Users can upload and manage their own documents, which are used as context for the chatbot's responses.

Each user's conversation history and context documents are securely stored and persist across sessions.

## Demo video

https://github.com/user-attachments/assets/df813c78-3b9b-4d88-aa85-8c6f8b269c81

## Features

- User registration/ log in
- Chat interface with RAG-powered responses
- Document upload and processing
- Persistent conversation history
- Admin interface for managing users and documents

## Project Structure

- `src/` - Main Django project directory
  - `accounts/` - User authentication and management
  - `chat/` - Chatbot logic, RAG pipeline, chat views
  - `documents/` - Document upload, processing, and management
  - `core/` - Project settings and URLs
  - `config/` - Configuration files
  - `media/` - Uploaded documents
  - `static/` - Static files (CSS, JS, images)
  - `templates/` - HTML templates

## Setup Instructions

### Prerequisites

- Python 3.11+
- [Poetry](https://python-poetry.org/) for dependency management
- SQLite (default) or another supported database

### Installation

1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd django-rag-chatbot
   ```
2. Install dependencies:
   ```bash
   poetry install
   ```
3. Apply migrations:
   ```bash
   poetry run python src/manage.py migrate
   ```
4. Create a superuser (optional, for admin access):
   ```bash
   poetry run python src/manage.py createsuperuser
   ```
5. Run the development server:
   ```bash
   poetry run python src/manage.py runserver
   ```

### Configuration

- Edit `src/config/settings.toml` for custom settings.
- Create a `src/config/.secrets.toml` and add an openrouter.ai API key.
- Uploaded documents are stored in `src/media/documents/` by default.

## Usage

- Access the app at `http://127.0.0.1:8000/`
- Register or log in to use the chatbot and document features.
- Admin interface: `http://127.0.0.1:8000/admin/`

## Testing

Run tests with:

```bash
poetry run python src/manage.py test
```

## License

MIT License

## Acknowledgements

- Django
- ChromaDB
- DeepSeek V3 0324 (via https://openrouter.ai/)

## Production Deployment with Docker

This project includes a `Dockerfile` ready for production use with Gunicorn as the WSGI server.

To run the Django server in a production environment using Docker:

1. Build the Docker image:
   ```bash
   docker build -t django-rag-chatbot .
   ```
2. Run the container (replace `<your-secret-key>` and configure environment variables as needed):
   ```bash
   docker run -d \
     -e DJANGO_SECRET_KEY=<your-secret-key> \
     -e DJANGO_ALLOWED_HOSTS=yourdomain.com \
     -p 8000:8000 \
     -v $(pwd)/src/media:/app/src/media \
     --name rag-chatbot \
     django-rag-chatbot
   ```
   - The `DJANGO_SECRET_KEY` and `DJANGO_ALLOWED_HOSTS` environment variables are required for production security.
   - The `-v $(pwd)/src/media:/app/src/media` option mounts the media directory for persistent file uploads.
3. Static files are automatically collected during the build process and served from `/app/static/`.
4. By default, the container starts Gunicorn with 3 workers. You can adjust this in the `Dockerfile` or override the `CMD` as needed.
5. For a full production setup, use a reverse proxy (e.g., Nginx) in front of the container to handle SSL termination and serve static/media files efficiently.

See the `Dockerfile` for build details and customize as required for your environment.

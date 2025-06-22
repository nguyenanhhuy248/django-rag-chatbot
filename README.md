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
- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/) (for containerized setup)

### Installation (Local Development)

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
- Create a `src/config/.secrets.toml` and add your OpenRouter API key and any other secrets.
- Uploaded documents are stored in `src/media/documents/` by default.

## Usage

- Access the app at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- Register or log in to use the chatbot and document features.
- Admin interface: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

## Testing

Run tests with:

```bash
poetry run python src/manage.py test
```

## Running with Docker Compose

This project provides a `docker-compose.yml` for easy local development and production setup, including the HuggingFace Embedding Inference (HFEI) reranker service.

### Quick Start

1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd django-rag-chatbot
   ```
2. Create a `src/config/.secrets.toml` file and add your secrets (e.g., `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`, OpenRouter API key, etc.).
3. Start all services (Django app and HFEI reranker):

   ```bash
   docker compose up --build
   ```

   This will:

   - Build and start the Django RAG chatbot server
   - Start the HuggingFace reranker server (HFEI) at `http://127.0.0.1:8080/rerank`

4. Access the app at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

### Secrets and Environment Variables

- All secrets and sensitive configuration should be placed in `src/config/.secrets.toml` (not `.env`).
- Example `src/config/.secrets.toml`:
  ```toml
  DJANGO_SECRET_KEY = "your-secret-key"
  DJANGO_ALLOWED_HOSTS = "localhost,127.0.0.1"
  openrouter_api_key = "your-openrouter-key"
  ```

### Stopping the Services

```bash
docker compose down
```

### Notes

- Uploaded documents are stored in `src/media/documents/` (mounted as a volume).
- The HFEI reranker uses the `BAAI/bge-reranker-base` model by default. You can change the model in `docker-compose.yml` if needed.
- For production, review and adjust secrets, environment variables, and Docker settings as appropriate.

## License

MIT License

## Acknowledgements

- Django
- ChromaDB
- DeepSeek V3 0324 (via https://openrouter.ai/)
- HuggingFace Text Embeddings Inference

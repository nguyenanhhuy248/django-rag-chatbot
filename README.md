# django-chatbot-rag

A Django-based Retrieval-Augmented Generation (RAG) chatbot application. This project integrates Django with a RAG pipeline to provide intelligent, context-aware chat capabilities, document management, and user authentication.

## Demo video

https://github.com/user-attachments/assets/df813c78-3b9b-4d88-aa85-8c6f8b269c81



## Features

- User authentication and registration
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

- Edit `src/config/settings.toml` and `src/core/settings.py` for custom settings.
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

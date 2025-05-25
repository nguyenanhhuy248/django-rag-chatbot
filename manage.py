#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
from __future__ import annotations

import os
import sys
from pathlib import Path


def main():
    """Run administrative tasks."""
    # Add the src directory to the Python path
    src_path = Path(__file__).resolve().parent / 'src'
    sys.path.insert(0, str(src_path))

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed?",
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

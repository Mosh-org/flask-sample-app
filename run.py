"""Entry point for running the Flask development server.

Reads the ``PORT`` environment variable (default ``5001``) and starts the
application on all interfaces when executed as a script.
"""

import os

from app import app

if __name__ == '__main__':
    port: int = int(os.environ.get("PORT", 5001)) # Default to 5001 if PORT env var is not set
    app.run(host='0.0.0.0', port=port)

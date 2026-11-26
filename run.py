"""Entry point for running the Flask sample app's development server.

Starts the application on the port given by the ``PORT`` environment
variable, defaulting to 5001.
"""

import os

from app import app

DEFAULT_PORT = 5001


def get_port() -> int:
    """Resolve the port the server should listen on.

    Returns:
        The integer value of the ``PORT`` environment variable, or
        ``DEFAULT_PORT`` when it is not set.
    """
    return int(os.environ.get("PORT", DEFAULT_PORT))


def main() -> None:
    """Run the Flask development server on all interfaces."""
    app.run(host='0.0.0.0', port=get_port())


if __name__ == '__main__':
    main()

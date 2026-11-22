"""Flask application package.

Creates the shared Flask app instance, configures rotating file logging, and
registers the routes.
"""

from __future__ import annotations

import logging
import os
import platform
from logging.handlers import RotatingFileHandler

from flask import Flask

#: The shared Flask application instance.
app: Flask = Flask(__name__)

log_dir: str = os.path.join(os.path.expanduser("~"), ".flask_sample_app")
os.makedirs(log_dir, exist_ok=True)
log_file: str = os.path.join(log_dir, "flask_sample_app.log")

file_handler: RotatingFileHandler = RotatingFileHandler(log_file, maxBytes=1_048_576, backupCount=5)
file_handler.setFormatter(logging.Formatter(
    "%(asctime)s %(levelname)s [%(name)s] %(message)s"
))
file_handler.setLevel(logging.INFO)

app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

app.logger.info(
    "Application starting — host=%s, platform=%s, log_file=%s",
    platform.node(), platform.system(), log_file,
)

# Imported last (after ``app`` exists) to avoid a circular import; the import
# registers the route handlers on ``app``.
from app import routes

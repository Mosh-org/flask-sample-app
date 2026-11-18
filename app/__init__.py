"""Flask sample app package.

Creates the module-level Flask application and configures file logging.

Importing this package has side effects:

* Creates the ``~/.flask_sample_app`` log directory if it does not exist.
* Attaches a rotating file handler (INFO level, 1 MiB per file, 5 backups)
  to ``app.logger``.
* Logs an "Application starting" message with host and platform details.
* Imports :mod:`app.routes` to register the HTTP routes.

Attributes:
    app: The Flask application instance.
    log_dir: Directory holding the application log file.
    log_file: Full path of the application log file.
    file_handler: Rotating file handler attached to ``app.logger``.
"""
import logging
import os
import platform
from logging.handlers import RotatingFileHandler

from flask import Flask

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

# Imported last on purpose: app.routes does `from app import app`, so the
# `app` object above must already exist (circular import). Do not move.
from app import routes

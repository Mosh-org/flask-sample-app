"""Unit tests for the port resolution and entry point in ``run.py``."""

import os
import unittest
from unittest import mock

import run


class TestRun(unittest.TestCase):
    """Tests for ``run.get_port`` and ``run.main``."""

    def test_get_port_default(self) -> None:
        """``get_port`` falls back to ``DEFAULT_PORT`` when ``PORT`` is unset."""
        with mock.patch.dict(os.environ, {}, clear=True):
            self.assertEqual(run.get_port(), 5001)

    def test_get_port_from_env(self) -> None:
        """``get_port`` returns the integer value of ``PORT``."""
        with mock.patch.dict(os.environ, {"PORT": "8080"}):
            self.assertEqual(run.get_port(), 8080)

    def test_get_port_invalid(self) -> None:
        """A non-integer ``PORT`` raises ``ValueError``."""
        with mock.patch.dict(os.environ, {"PORT": "abc"}):
            with self.assertRaises(ValueError):
                run.get_port()

    def test_main_runs_app(self) -> None:
        """``main`` starts the app on all interfaces with the resolved port."""
        with mock.patch.dict(os.environ, {"PORT": "6000"}):
            with mock.patch.object(run.app, "run") as mock_run:
                run.main()
        mock_run.assert_called_once_with(host="0.0.0.0", port=6000)


if __name__ == "__main__":
    unittest.main()

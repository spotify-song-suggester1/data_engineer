#!/usr/bin/env python
"""
Entry point for Flask web application
"""

from .app import create_app

APP = create_app()
#!/usr/bin/env python3
"""
For WSGI Server
To run:
$ gunicorn -b 0.0.0.0:5000 wsgi:app
OR
$ export FLASK_APP=wsgi
$ flask run
"""
import os
from app import create_app

env = os.environ.get('app_ENV', 'prod')
app = create_app('app.settings.%sConfig' % env.capitalize())

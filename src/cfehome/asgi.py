# With this module we are no longer using the wsgi and now we are using the asgi. This is especially done for production
import os
import django
from channels.routing import get_default_application

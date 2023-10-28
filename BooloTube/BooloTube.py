"""Welcome to Reflex!."""

from BooloTube import styles

# Import all the pages.
from BooloTube.pages import *

import reflex as rx
from .api.project import project_router
from .api.timestamp import timestamp_router

# Create the app and compile it.
app = rx.App(style=styles.base_style)
app.api.include_router(project_router)
app.api.include_router(timestamp_router)
app.compile()

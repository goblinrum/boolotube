import reflex as rx
import os
from dotenv import load_dotenv

load_dotenv()

config = rx.Config(
    app_name="BooloTube",
    db_url=os.getenv('db_url')
)
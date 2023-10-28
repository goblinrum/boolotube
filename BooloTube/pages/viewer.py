import httpx
import reflex as rx
from BooloTube.templates import template
from BooloTube.state import State
from fastapi import Request
import requests

@template(route="/viewer/{project_id}", title="Viewer")
def viewer() -> rx.Component:
    project_id = State.project_id
    project = fetch_project(project_id)
    timestamps = fetch_timestamps(project_id)
    return rx.container(
        video_container(project),
        timestamps_list(timestamps)
    )

def iframe_component(src: str, width: str = "100%", height: str = "100%") -> rx.Component:
    return rx.html(f'<iframe src="{src}" width="{width}" height="{height}"></iframe>')

def video_container(project: dict) -> rx.Component:
    return rx.hstack(
        iframe_component(src=project["my_reaction_url"], width="48%", height="315"),
        iframe_component(src=project["original_video_url"], width="48%", height="315")
    )

def timestamps_list(timestamps: list) -> rx.Component:
    return rx.ul(
        [rx.li(f'My Reaction: {ts["start_time_my_reaction"]} - {ts["end_time_my_reaction"]} maps to Original: {ts["start_time_original"]} - {ts["end_time_original"]}') for ts in timestamps]
    )

def fetch_project(project_id):
    with httpx.Client() as client:
        response = client.get(f"http://localhost:8000/project/{project_id}")
        if response.status_code == 200:
            return response.json()
        else:
            return None

def fetch_timestamps(project_id):
    with httpx.Client() as client:
        response = client.get(f"http://localhost:8000/timestamps/{project_id}")
        if response.status_code == 200:
            return response.json()
        else:
            return []

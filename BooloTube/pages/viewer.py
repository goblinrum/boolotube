import httpx
import reflex as rx
from BooloTube.templates import template
from BooloTube.state import State
import json
from typing import Optional, Dict, Any
import httpx

class ViewerState(State):

    project: Dict[str, Any] = {}
    my_reaction_url = ""
    original_video_url = ""

    @rx.background
    async def fetch_project(self):
        project_id = self.project_id
        print("project_id", project_id)
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://localhost:8000/project/{project_id}")
            if response.status_code == 200:
                async with self:
                    self.project = response.json()
                    self.my_reaction_url = self.project['my_reaction_url']
                    self.original_video_url = self.project['original_video_url']
                    print("code", self.project)
                yield

    # async def fetch_timestamps(self, project_id):
    #     async with httpx.AsyncClient() as client:
    #         response = await client.get(f"http://localhost:8000/timestamps/{project_id}")
    #         if response.status_code == 200:
    #             return response.json()
    #         else:
    #             return []

@template(route="/viewer/[q]", title="Viewer", on_load=ViewerState.fetch_project)
def viewer() -> rx.Component:
    return video_container()
        # timestamps_list(timestamps)
    

def iframe_component(src: str, width: str = "100%", height: str = "100%") -> rx.Component:
    return rx.html(f'<iframe src="{src}" width="{width}" height="{height}"></iframe>')

def video_container() -> rx.Component:
    return rx.hstack( 
        rx.video(
            url = ViewerState.my_reaction_url,
            width = "220",
            height = "300",
        ),
        rx.video(
            url = ViewerState.original_video_url,
            width = "220",
            height = "300",
        ),
    )

def timestamps_list(timestamps: list) -> rx.Component:
    return rx.ul(
        [rx.li(f'My Reaction: {ts["start_time_my_reaction"]} - {ts["end_time_my_reaction"]} maps to Original: {ts["start_time_original"]} - {ts["end_time_original"]}') for ts in timestamps]
    )


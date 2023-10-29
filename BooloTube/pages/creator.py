import reflex as rx
from BooloTube.templates import template
from BooloTube.state import State
import json
from typing import Optional, Dict, Any
import httpx
from functools import partial

class FormState(State):
    project: Dict[str, Any] = {}
    
    @rx.background
    async def fetch_project(self):
        secret_id = self.secret_id
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://localhost:8000/project_s/{secret_id}")
            if response.status_code == 200:
                async with self:
                    self.project = response.json()
                    self.response_p = self.project['uuid']
                    self.reaction_url = self.project['my_reaction_url']
                    self.original_url = self.project['original_video_url']
                    self.secret = self.project['secret_id']
                    async with httpx.AsyncClient() as client:  
                        response = await client.get(f"http://localhost:8000/timestamps/{self.response_p}")
                        if response.status_code == 200:
                            self.timestamp_items_list = response.json()["result"]
                yield
            else:
                async with self:
                    self.err=response.json()['detail']
                    self.reaction_url=''
                    self.original_url=''
                    self.reaction_url_start=''
                    self.reaction_url_end=''
                    self.original_url_start=''
                    self.original_url_end=''
                    
                    self.form_data_p={}
                    self.response_p=None
                    self.form_data_t={}
                    self.reaction_url_end=None
                    self.secret=None
                    self.timestamp_list=None

    reaction_url: str = ''
    original_url: str = ''
    reaction_url_start: str = ''
    reaction_url_end: str = ''
    original_url_start: str = ''
    original_url_end: str = ''

    form_data_p: Dict[str, Any] = {}
    response_p: Optional[str] = None
    form_data_t: Dict[str, Any] = {}
    response_t: Optional[str] = None
    err: Optional[str] = None
    secret: Optional[str] = None
    timestamp_items_list: list[dict] = []

    def reset_state(self):
        self.form_data_p={}
        self.response_p=None
        self.form_data_t={}
        self.response_t=None
        self.err=None
        self.reaction_url = ""
        self.original_url = ""
        self.reaction_url_start = ""
        self.reaction_url_end = ""
        self.original_url_start = ""
        self.original_url_end = ""

    async def delete_timestamp(self, timestamp_uuid):
        async with httpx.AsyncClient() as client:  
            response = await client.delete(f"http://localhost:8000/timestamp/{timestamp_uuid}")
            if response.status_code == 200:
                async with httpx.AsyncClient() as client:  
                    responsees = await client.get(f"http://localhost:8000/timestamps/{self.response_p}")
                    if responsees.status_code == 200:
                        self.timestamp_items_list = responsees.json()["result"]

    async def handle_submit_p(self, form_data: dict):
        self.form_data_p = form_data
        async with httpx.AsyncClient() as client:
            response = await client.post("http://localhost:8000/project", data=json.dumps(form_data))
        if response.status_code==400:
            self.err = response.json()['detail']
        else:
            self.response_p = response.json()['project_id']
            self.err = None
            self.secret=response.json()['secret_id']

    async def handle_submit_t(self, form_data: dict):
        form_data['project_id'] = self.response_p
        self.form_data_t = form_data
        async with httpx.AsyncClient() as client:
            response = await client.post("http://localhost:8000/timestamp", data=json.dumps(form_data))
        if response.status_code==400:
            self.err = response.json()['detail']
        else:
            self.response_t = response.json()['timestamp_id']
            self.err = None

        async with httpx.AsyncClient() as client:  
            response = await client.get(f"http://localhost:8000/timestamps/{self.response_p}")
            if response.status_code == 200:
                self.timestamp_items_list = response.json()["result"]

    
@template(route="/creator/[pid]", title="Creator", on_load=FormState.fetch_project)
def creator() -> rx.Component:
    return rx.vstack(
        project_form(),
        rx.cond(FormState.response_p,
                rx.text("Your secret_id is: ", FormState.secret, ". Write this down.")),
        rx.cond(FormState.response_p,
                rx.text("Your product_id is: ", FormState.response_p, ". Write this down.")),
        rx.cond(FormState.response_p,
               timestamp_form()),
        rx.cond(FormState.err,
                rx.text(FormState.err)),
        rx.button(
            "Make New",
            on_click=FormState.reset_state())
    )

def project_form() -> rx.Component:
    return rx.vstack(
        rx.form(
            rx.vstack(
                rx.text("My Reaction URL:", rx.cond(~FormState.response_p,
                    rx.input(type="text", id="my_reaction_url", on_change=FormState.set_reaction_url, value=FormState.reaction_url),
                    rx.input(type="text", id="my_reaction_url", on_change=FormState.set_reaction_url, value=FormState.reaction_url, is_disabled=True))),
                rx.text("Original Video URL:", rx.cond(~FormState.response_p,
                    rx.input(type="text", id="original_video_url", on_change=FormState.set_original_url, value=FormState.original_url),
                    rx.input(type="text", id="original_video_url", on_change=FormState.set_original_url, value=FormState.original_url, is_disabled=True))),
                rx.cond(~FormState.response_p,
                    rx.button("Submit", type_="submit"),
                    rx.button("Submit", type_="submit", is_disabled=True)),
            ),
            on_submit=FormState.handle_submit_p,
        ),
    )

def timestamp_form() -> rx.Component:
    return rx.vstack(
        rx.form(
            rx.vstack(
                rx.text("Start Time My Reaction:", rx.input(type="text", id="start_time_my_reaction", on_change=FormState.set_reaction_url_start, value=FormState.reaction_url_start)),
                rx.text("End Time My Reaction:", rx.input(type="text", id="end_time_my_reaction", on_change=FormState.set_reaction_url_end, value=FormState.reaction_url_end)),
                rx.text("Start Time Original:", rx.input(type="text", id="start_time_original", on_change=FormState.set_original_url_start, value=FormState.original_url_start)),
                rx.text("End Time Original:", rx.input(type="text", id="end_time_original", on_change=FormState.set_original_url_end, value=FormState.original_url_end)),
                rx.button("Submit", type_="submit"),
            ),
            on_submit=FormState.handle_submit_t,  
        ),
rx.box(
        rx.foreach(FormState.timestamp_items_list, lambda timestamp: rx.vstack(rx.hstack(rx.text(f'Start Time My Reaction: {timestamp["start_time_my_reaction"]}'),rx.text(f'End Time My Reaction: {timestamp["end_time_my_reaction"]}')),rx.hstack(rx.text(f'Start Time Original: {timestamp["start_time_original"]}'),rx.text(f'End Time Original: {timestamp["end_time_original"]}')), rx.button(f"Delete", on_click=partial(FormState.delete_timestamp, timestamp['uuid']))))
)
    )

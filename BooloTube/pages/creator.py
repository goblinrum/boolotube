import reflex as rx
from BooloTube.templates import template
from BooloTube.state import State
import json
from typing import Optional, Dict, Any
import httpx

@template(route="/creator", title="Creator")
def creator() -> rx.Component:
    return rx.vstack(
        project_form(),
        rx.cond(FormState.response_p,
               timestamp_form()),
        rx.cond(FormState.err,
                rx.text(FormState.err)),
        rx.button(
            "Make New",
            on_click=FormState.reset_state())
    )


class FormState(State):

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

    async def handle_submit_p(self, form_data: dict):
        self.form_data_p = form_data
        async with httpx.AsyncClient() as client:
            response = await client.post("http://localhost:8000/project", data=json.dumps(form_data))
        if response.status_code==400:
            self.err = response.json()['detail']
        else:
            self.response_p = response.json()['project_id']
            self.err = None

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
    )

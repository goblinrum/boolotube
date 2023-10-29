from BooloTube.templates import template

import reflex as rx
from BooloTube.state import State

class SearchState(State):
    secret_id2: str = '' 

@template(route="/search", title="Search")
def search() -> rx.Component:
    return rx.vstack(
        rx.form(
            rx.vstack(
                rx.text("Find Existing Secret ID:", rx.input(type="text", id="secret_id2", on_change=SearchState.set_secret_id2, value=SearchState.secret_id2)),
                rx.button("Submit", type_="submit", on_click=rx.redirect(f"/creator/{SearchState.secret_id2}")),
            )
        ),
    )

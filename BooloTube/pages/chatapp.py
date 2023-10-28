import reflex as rx

from BooloTube.templates import template
from BooloTube.state import State

def qa(question: str, answer: str) -> rx.Component:
    return rx.box(
        rx.box(
            rx.text(question, text_align="right"),
        ),
        rx.box(
            rx.text(answer, text_align="left"),
        ),
        margin_y="1em",
    )


def chat() -> rx.Component:
    return rx.box(
        rx.foreach(
            State.chat_history,
            lambda messages: qa(messages[0], messages[1]),
        )
    )


def action_bar() -> rx.Component:
    return rx.hstack(
        rx.input(
            value=State.question,
            placeholder="Ask a question",
            on_change=State.set_question,
        ),
        rx.button(
            "Ask",
            on_click=State.answer,
        ),
    )

@template(route="/chat", title="Chat")
def chatapp() -> rx.Component:
    return rx.container(
        chat(),
        action_bar(),
    )


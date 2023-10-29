"""Base state for the app."""

import reflex as rx

class State(rx.State):

    @rx.var
    def project_id(self) -> str:
        return self.get_query_params().get('q', 'no pid')
        

    @rx.var
    def secret_id(self) -> str:
        return self.get_query_params().get('pid', 'no pid')

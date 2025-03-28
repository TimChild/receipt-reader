"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import asyncio
from typing import AsyncIterator

import reflex as rx
from reflex.event import EventType

from rxconfig import config


class State(rx.State):
    """The app state."""

    running: bool = False

    @rx.event(background=True)
    async def on_drop_process_receipt(self, files: rx.UploadFile) -> AsyncIterator[EventType]:
        """Process the receipt."""
        _ = files
        async with self:
            if self.running:
                return
            self.running = True
        # -- self.running gets updated

        try:
            yield rx.toast.info("Processing receipt...")

            await asyncio.sleep(2)
            # Do the processing here

            yield rx.toast.info("Receipt processed!")

        finally:
            async with self:
                self.running = False

        return


def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.button("Demo upload", on_click=lambda: State.on_drop_process_receipt(None)),  # pyright: ignore[reportArgumentType]
            rx.upload(on_drop=State.on_drop_process_receipt, multiple=False),
            rx.heading("Welcome to Reflex!", size="9"),
            rx.text(
                "Get started by editing ",
                rx.code(f"{config.app_name}/{config.app_name}.py"),
                size="5",
            ),
            rx.link(
                rx.button("Check out our docs!"),
                href="https://reflex.dev/docs/getting-started/introduction/",
                is_external=True,
            ),
            spacing="5",
            justify="center",
            min_height="85vh",
        ),
        rx.logo(),
    )


app = rx.App()
app.add_page(index)

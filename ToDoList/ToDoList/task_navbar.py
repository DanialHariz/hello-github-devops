#task_navbar.py

import reflex as rx

def navbar():
    return rx.flex(
        # Logo badge on the left
        rx.badge(
            rx.icon(tag="notebook-pen", size=28),
            rx.heading("Task Manager App", size="6"),
            color_scheme="blue",
            radius="large",
            align="center",
            variant="surface",
            padding="0.65rem",
        ),
        rx.spacer(),
        # Right-side tools
        rx.hstack(
            rx.button(
                "Tasks",
                variant="solid",
                color_scheme="blue",
                size="3",
            ),
            rx.color_mode.button(),
            align="center",
            spacing="3",
        ),
        spacing="2",
        flex_direction=["column", "column", "row"],
        align="center",
        width="100%",
        top="0px",
        padding_top="2em",
        padding_x="2em",
    )

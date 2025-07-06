#task_table.py

import reflex as rx
from .state import TaskState


def status_badge(status: str):
    color = rx.cond(
        status == "complete",
        "green",
        rx.cond(
            status == "overdue",
            "red",
            "orange",
        ),
    )
    label = rx.cond(
        status == "complete",
        "Complete",
        rx.cond(
            status == "overdue",
            "Overdue",
            "Pending",
        ),
    )
    return rx.badge(label, color_scheme=color, radius="full", size="2")


def show_task(task):
    toggle_label = rx.cond(
        task["status"] == "complete",
        "Undo",
        "Complete",
    )
    toggle_color = rx.cond(
        task["status"] == "complete",
        "blue",
        "green",
    )
    return rx.table.row(
        rx.table.cell(task["title"]),
        rx.table.cell(task["description"]),
        rx.table.cell(task["due_date"]),
        rx.table.cell(status_badge(task["status"])),
        rx.table.cell(
            rx.hstack(
                rx.button(
                    toggle_label,
                    size="2",
                    color_scheme=toggle_color,
                    on_click=lambda: TaskState.toggle_complete(task["_id"]),
                ),
                rx.button(
                    "Edit",
                    size="2",
                    color_scheme="amber",
                    on_click=lambda: TaskState.load_task_for_edit(task["_id"]),
                ),
                rx.button(
                    "Delete",
                    size="2",
                    color_scheme="red",
                    on_click=lambda: TaskState.delete_task(task["_id"]),
                ),
            )
        ),
        style={"_hover": {"bg": rx.color("gray", 3)}},
        align="center",
    )


def _header_cell(text: str, icon: str):
    return rx.table.column_header_cell(
        rx.hstack(
            rx.icon(icon, size=18),
            rx.text(text),
            align="center",
            spacing="2",
        )
    )


def task_table():
    return rx.fragment(
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    _header_cell("Title", "type"),
                    _header_cell("Description", "file-text"),
                    _header_cell("Due Date", "calendar"),
                    _header_cell("Status", "info"),
                    _header_cell("Actions", "cog"),
                )
            ),
            rx.table.body(
                # Inline Add/Edit row
                # Existing tasks
                rx.foreach(TaskState.tasks, show_task),
                rx.table.row(
                    rx.table.cell(
                        rx.input(
                            placeholder="Title",
                            value=TaskState.title,
                            on_change=TaskState.set_title,
                            size="2",
                        )
                    ),
                    rx.table.cell(
                        rx.input(
                            placeholder="Description",
                            value=TaskState.description,
                            on_change=TaskState.set_description,
                            size="2",
                        )
                    ),
                    rx.table.cell(
                        rx.input(
                            placeholder="YYYY-MM-DD",
                            type_="date",
                            value=TaskState.due_date,
                            on_change=TaskState.set_due_date,
                            size="2",
                        )
                    ),
                    rx.table.cell("-"),
                    rx.table.cell(
                        rx.button(
                            rx.cond(
                                TaskState.editing_id != "",
                                "Save",
                                "Add Task"
                            ),
                            size="2",
                            color_scheme=rx.cond(
                                TaskState.editing_id != "",
                                "green",
                                "blue",
                            ),
                            on_click=rx.cond(
                                TaskState.editing_id != "",
                                TaskState.save_task,
                                TaskState.add_task
                            )
                        )
                    ),
                ),                           
            ),
            variant="surface",
            size="3",
            width="100%",
            on_mount=TaskState.load_tasks,
        )
    )

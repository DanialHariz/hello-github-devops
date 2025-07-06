# ToDoList.py
import reflex as rx
from .task_table import task_table
from .task_navbar import navbar
from .state import TaskState  # ✅ DB-backed state

def task_item(task):
    status = task["status"]

    status_component = rx.cond(
        status == "complete",
        rx.text("✅ Complete", color="green"),
        rx.cond(
            status == "overdue",
            rx.text("⚠️ Overdue", color="red"),
            rx.text("⏳ Pending", color="orange"),
        )
    )

    toggle_label = rx.cond(
        status == "complete",
        "Undo",
        "Complete",
    )

    toggle_color = rx.cond(
        status == "complete",
        "blue",   
        "grass"   
    )

    return rx.box(
        rx.text(task["title"], font_weight="bold"),
        rx.text(task["description"]),
        rx.text(f"Due: {task['due_date']}"),
        status_component,
        rx.hstack(
            rx.button(
                toggle_label,
                on_click=lambda: TaskState.toggle_complete(task["_id"]),
                color_scheme=toggle_color  # ✅ dynamic color scheme!
            ),
            rx.button(
                "Edit",
                on_click=lambda: TaskState.load_task_for_edit(task["_id"]),
                color_scheme="amber"
            ),
            rx.button(
                "Delete",
                on_click=lambda: TaskState.delete_task(task["_id"]),
                color_scheme="red",
            )
        ),
        border="1px solid #ccc",
        padding="1em",
        margin_bottom="1em",
        border_radius="0.5em",
    )



def index():
    return rx.vstack(
        navbar(),
        rx.divider(),
        task_table(),
        spacing="4",
    )



app = rx.App()
app.add_page(index)

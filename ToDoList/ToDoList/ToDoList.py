import reflex as rx
import datetime

class Task(rx.Base):
    id: int
    title: str
    description: str
    due_date: datetime.date
    status: str  # "pending" or "complete"

class State(rx.State):
    tasks: list[Task] = []
    next_id: int = 1

    # Fields for input
    title: str = ""
    description: str = ""
    due_date: str = ""
    editing_id: int | None = None

    def add_task(self):
        new_task = Task(
            id=self.next_id,
            title=self.title,
            description=self.description,
            due_date=datetime.date.fromisoformat(self.due_date),
            status="pending",
        )
        self.tasks.append(new_task)
        self.next_id += 1
        self.clear_inputs()

    def edit_task(self, task_id: int):
        task = next(t for t in self.tasks if t.id == task_id)
        self.title = task.title
        self.description = task.description
        self.due_date = str(task.due_date)
        self.editing_id = task_id

    def save_task(self):
        for i, t in enumerate(self.tasks):
            if t.id == self.editing_id:
                self.tasks[i] = Task(
                    id=t.id,
                    title=self.title,
                    description=self.description,
                    due_date=datetime.date.fromisoformat(self.due_date),
                    status=t.status,
                )
                break
        self.clear_inputs()

    def delete_task(self, task_id: int):
        self.tasks = [t for t in self.tasks if t.id != task_id]

    def toggle_complete(self, task_id: int):
        for i, t in enumerate(self.tasks):
            if t.id == task_id:
                self.tasks[i].status = (
                    "complete" if t.status != "complete" else "pending"
                )
                break

    def clear_inputs(self):
        self.title = ""
        self.description = ""
        self.due_date = ""
        self.editing_id = None

def task_item(task: Task):
    is_complete = task.status == "complete"
    is_overdue = (task.due_date < datetime.date.today()) & ~is_complete

    status_component = rx.cond(
        is_complete,
        rx.text("✅ Complete", color="green"),
        rx.cond(
            is_overdue,
            rx.text("⚠ Overdue", color="red"),
            rx.text("⏳ Pending", color="orange"),
        ),
    )

    return rx.box(
        rx.text(task.title, font_weight="bold"),
        rx.text(task.description),
        rx.text(f"Due: {task.due_date}"),
        status_component,
        rx.button("Edit", on_click=lambda: State.edit_task(task.id)),
        rx.button("Delete", on_click=lambda: State.delete_task(task.id)),
        rx.button(
            "Toggle Complete",
            on_click=lambda: State.toggle_complete(task.id),
        ),
        border="1px solid #ccc",
        padding="1em",
        margin_bottom="1em",
        opacity=rx.cond(is_complete, "0.5", "1.0"),
    )

def index():
    return rx.vstack(
        rx.heading("📋Todo App"),
        rx.input(placeholder="Title", value=State.title, on_change=State.set_title),
        rx.text_area(
            placeholder="Description",
            value=State.description,
            on_change=State.set_description,
        ),
        rx.input(
            type_="date",
            placeholder="YYYY-MM-DD",
            value=State.due_date,
            on_change=State.set_due_date,
        ),
        rx.button(
            rx.cond(State.editing_id, "Save", "Add Task"),
            on_click=rx.cond(State.editing_id, State.save_task, State.add_task),
        ),
        rx.foreach(State.tasks, task_item),
    )

app = rx.App()
app.add_page(index)
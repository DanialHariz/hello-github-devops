#state.py
from datetime import datetime
from pymongo import MongoClient
import reflex as rx
from typing import List, Dict, Any
from bson.objectid import ObjectId

# MongoDB connection
MONGO_URI = "mongodb+srv://humairabeseek:vbBNf7klEdIVko4W@cluster0.kzkc86t.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client["ToDo"]
tasks_collection = db["tasks"]

class TaskState(rx.State):
    tasks: List[Dict[str, Any]] = []
    title: str = ""
    description: str = ""
    due_date: str = ""
    editing_id: str = ""

    def load_tasks(self):
        self.tasks = []
        today = datetime.now().date()

        for task in tasks_collection.find():
            task["_id"] = str(task["_id"])
            due_date_str = task.get("due_date", "")

            try:
                due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
            except Exception:
                due_date = None

            # Check if overdue
            if due_date and due_date < today and task["status"] == "pending":
                task["status"] = "overdue"
                tasks_collection.update_one(
                    {"_id": ObjectId(task["_id"])},
                    {"$set": {"status": "overdue"}}
                )

            self.tasks.append(task)

    def add_task(self):
        if self.title:
            tasks_collection.insert_one({
                "title": self.title,
                "description": self.description,
                "due_date": self.due_date,
                "status": "pending"
            })
            self.clear_form()
            self.load_tasks()

    def toggle_complete(self, task_id: str):
        task = tasks_collection.find_one({"_id": ObjectId(task_id)})
        if task:
            current_status = task["status"]
            # If overdue, allow toggle only to complete
            if current_status == "overdue":
                new_status = "complete"
            else:
                new_status = "pending" if current_status == "complete" else "complete"

            tasks_collection.update_one(
                {"_id": ObjectId(task_id)},
                {"$set": {"status": new_status}}
            )
            self.load_tasks()

    def delete_task(self, task_id: str):
        tasks_collection.delete_one({"_id": ObjectId(task_id)})
        self.load_tasks()

    def load_task_for_edit(self, task_id: str):
        task = tasks_collection.find_one({"_id": ObjectId(task_id)})
        if task:
            self.editing_id = task_id
            self.title = task["title"]
            self.description = task["description"]
            self.due_date = task["due_date"]

    def save_task(self):
        if self.editing_id:
            tasks_collection.update_one(
                {"_id": ObjectId(self.editing_id)},
                {"$set": {
                    "title": self.title,
                    "description": self.description,
                    "due_date": self.due_date
                }}
            )
            self.clear_form()
            self.load_tasks()

    def clear_form(self):
        self.editing_id = ""
        self.title = ""
        self.description = ""
        self.due_date = ""

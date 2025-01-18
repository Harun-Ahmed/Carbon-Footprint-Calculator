import json
from datetime import datetime

class TodoApp:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = self.load_tasks()

    def load_tasks(self):
        try:
            with open(self.filename, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_tasks(self):
        with open(self.filename, "w") as file:
            json.dump(self.tasks, file, indent=4)

    def display_tasks(self):
        if not self.tasks:
            print("No tasks to show.")
        else:
            print("\nYour To-Do List:")
            for index, task in enumerate(sorted(self.tasks, key=lambda x: x['priority'], reverse=True), start=1):
                due_date = task["due_date"] if task["due_date"] else "No due date"
                status = "Done" if task["done"] else "Not Done"
                print(f"{index}. {task['task']} [{status}] | Priority: {task['priority']} | Due: {due_date}")

    def add_task(self):
        task_name = input("\nEnter the task: ")
        priority = input("Enter priority (Low, Medium, High): ").capitalize()
        while priority not in ["Low", "Medium", "High"]:
            print("Invalid priority. Please choose from Low, Medium, or High.")
            priority = input("Enter priority (Low, Medium, High): ").capitalize()

        due_date_input = input("Enter due date (YYYY-MM-DD) or leave blank: ")
        due_date = None
        if due_date_input:
            try:
                due_date = datetime.strptime(due_date_input, "%Y-%m-%d").date()
            except ValueError:
                print("Invalid date format. Using 'No due date'.")
                due_date = None

        self.tasks.append({
            "task": task_name,
            "done": False,
            "priority": priority,
            "due_date": str(due_date) if due_date else None
        })
        print(f"Task '{task_name}' added!")
        self.save_tasks()

    def mark_task_done(self):
        self.display_tasks()
        try:
            task_index = int(input("\nEnter the task number to mark as done: ")) - 1
            if 0 <= task_index < len(self.tasks):
                self.tasks[task_index]["done"] = True
                print(f"Task '{self.tasks[task_index]['task']}' marked as done!")
                self.save_tasks()
            else:
                print("Invalid task number.")
        except ValueError:
            print("Please enter a valid task number.")

    def remove_task(self):
        self.display_tasks()
        try:
            task_index = int(input("\nEnter the task number to remove: ")) - 1
            if 0 <= task_index < len(self.tasks):
                removed_task = self.tasks.pop(task_index)
                print(f"Task '{removed_task['task']}' removed!")
                self.save_tasks()
            else:
                print("Invalid task number.")
        except ValueError:
            print("Please enter a valid task number.")

    def run(self):
        while True:
            print("\n--- To-Do List App ---")
            print("1. View Tasks")
            print("2. Add Task")
            print("3. Mark Task as Done")
            print("4. Remove Task")
            print("5. Exit")

            choice = input("\nEnter your choice: ")

            if choice == "1":
                self.display_tasks()
            elif choice == "2":
                self.add_task()
            elif choice == "3":
                self.mark_task_done()
            elif choice == "4":
                self.remove_task()
            elif choice == "5":
                print("Exiting the app.")
                break
            else:
                print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    todo_app = TodoApp()
    todo_app.run()


"""
Smart Task Management Engine
Author: Junaid
Description: An object-oriented task manager with automated priority calculation,
             persistent JSON storage, and productivity analytics.
"""

import datetime
import json


class Task:
    """
    Represents an individual task with its properties and metadata.
    """
    def __init__(self, title, description, deadline_days):
        self.title = title
        self.description = description
        self.status = "Pending"  # Default status for all new tasks
        self.priority = self.calculate_priority(deadline_days)
        
        # Calculate absolute deadline date from current date
        self.created_at = datetime.date.today()
        self.deadline = self.created_at + datetime.timedelta(days=deadline_days)

    def calculate_priority(self, deadline_days):
        """
        Automatically determines task priority based on remaining days.
        """
        if deadline_days <= 2:
            return "High"
        elif deadline_days <= 5:
            return "Medium"
        else:
            return "Low"

    def display_task(self):
        """
        Prints the task details in a clean, structured format.
        """
        print(f"Task Title : {self.title}")
        print(f"Description: {self.description}")
        print(f"Status     : {self.status} | Deadline: {self.deadline}")
        print(f"Priority   : {self.priority}")
        print("-" * 40)


class TaskManager:
    """
    Manages collection of tasks, handling CRUD operations and data persistence.
    """
    def __init__(self):
        self.tasks = []

    def add_task(self, title, description, deadline_days):
        """
        Creates a new task instance and appends it to the tracking list.
        """
        new_task = Task(title, description, deadline_days)
        self.tasks.append(new_task)
        print("Success: Task added successfully.")

    def view_all_tasks(self):
        """
        Displays all currently tracked tasks.
        """
        if not self.tasks:
            print("Notice: No tasks found in the system.")
            return 
        
        print("\n--- CURRENT TRACKED TASKS ---")
        for task in self.tasks:
            task.display_task()

    def mark_task_complete(self, title):
        """
        Searches for a task by title and updates its status to Completed.
        """
        for task in self.tasks:
            if task.title.lower() == title.lower():  # Case-insensitive comparison
                task.status = "Completed"
                print("Success: Task status updated to Completed.")
                return
        print("Error: Target task title not found.")

    def generate_productivity_report(self):
        """
        Calculates and outputs data-driven productivity performance analytics.
        """
        if not self.tasks:
            print("Notice: No task data available for analytics.")
            return

        total_tasks = len(self.tasks)
        completed_tasks = sum(1 for task in self.tasks if task.status == "Completed")
        
        # Calculate percentage metric
        productivity_score = (completed_tasks / total_tasks) * 100

        print("\n--- PRODUCTIVITY ANALYTICS REPORT ---")
        print(f"Total Tasks Managed   : {total_tasks}")
        print(f"Completed Tasks       : {completed_tasks}")
        print(f"Productivity Score   : {productivity_score:.2f}%")
        print("-------------------------------------")

    def save_to_file(self):
        """
        Serializes runtime task objects into JSON format for persistent storage.
        """
        formatted_tasks = []
        for task in self.tasks:
            task_dict = { 
                "title": task.title,
                "description": task.description,
                "status": task.status,
                "priority": task.priority,
                "deadline": str(task.deadline)  # ISO format string conversion
            }
            formatted_tasks.append(task_dict)

        with open("tasks.json", "w") as file:
            json.dump(formatted_tasks, file, indent=4)
        print("System: Runtime state serialized and saved to tasks.json.")

    def load_from_file(self):
        """
        Deserializes stored JSON data back into living runtime Task objects.
        """
        try:
            with open("tasks.json", "r") as file:
                saved_data = json.load(file)
                
                self.tasks = []  # Reset state before hydration
                for dict_task in saved_data:
                    # Instantiate object with placeholder deadline offset
                    new_task = Task(dict_task["title"], dict_task["description"], 0)
                    
                    # Hydrate saved properties
                    new_task.status = dict_task["status"]
                    new_task.priority = dict_task["priority"]
                    
                    # Parse string back to datetime object
                    new_task.deadline = datetime.datetime.strptime(dict_task["deadline"], "%Y-%m-%d").date()
                    self.tasks.append(new_task)
            print("System: State restoration successful. Database records loaded.")
        except FileNotFoundError:
            # Silent fallback if database file does not exist yet
            pass


# --- Main Runtime Loop Execution ---
if __name__ == "__main__":
    
    manager = TaskManager()
    manager.load_from_file()  # Automatic database hydration on startup
    
    while True:
        print("\n==== SMART TASK ENGINE INTERACTIVE INTERFACE ====")
        print("1. Create/Add New Task")
        print("2. View All Managed Tasks")
        print("3. Finalize Task (Mark Completed)")
        print("4. Fetch Productivity Analytics")
        print("5. Terminate Program")
        print("================================================")
        
        user_choice = input("Select an option (1-5): ").strip()
        
        if user_choice == "1":
            print("\n--- Task Creation Mode ---")
            title = input("Enter Task Title: ")
            description = input("Enter Task Description: ")
            
            # Validation handling for integer casting
            try:
                deadline_days = int(input("Enter Days Until Deadline: "))
                manager.add_task(title, description, deadline_days)
                manager.save_to_file()
            except ValueError:
                print("Error: Invalid numeric format for deadline days. Operation aborted.")

        elif user_choice == "2":
            manager.view_all_tasks()
            
        elif user_choice == "3":
            print("\n--- Task Resolution Mode ---")
            target_title = input("Enter the precise title of the completed task: ")
            manager.mark_task_complete(target_title)
            manager.save_to_file()
            
        elif user_choice == "4":
            manager.generate_productivity_report()
            
        elif user_choice == "5":
            print("\nSystem: Shutting down core engine. Sessions terminated. Goodbye.")
            break
            
        else:
            print("Error: Input out of bounds. Please select a valid option (1-5).")
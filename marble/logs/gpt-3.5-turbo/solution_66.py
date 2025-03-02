class Task:def check_dependencies_completed(self):
        for dependency in self.dependencies:
            if dependency.status != 'Completed':
                return False
        return Truedef add_dependency(self, task):
        self.dependencies.append(task)

    def __str__(self):
        return self.name


class TaskChain:
    def __init__(self):
        self.tasks = {}

    def create_task(self, name):
        task = Task(name)
        self.tasks[name] = task
        return task

    def get_task(self, name):
        return self.tasks.get(name)

    def mark_task_as_started(self, task_name, start_time):
        task = self.get_task(task_name)
        if task:
            task.status = "In Progress"
            task.start_time = start_time
        else:
            print("Task not found.")

    def mark_task_as_completed(self, task_name, end_time):
        task = self.get_task(task_name)
        if task:
            task.status = "Completed"
            task.end_time = end_time
        else:
            print("Task not found.")

    def generate_report(self):
        completed_tasks = []
        ongoing_tasks = []
        delayed_tasks = []

        for task_name, task in self.tasks.items():
            if task.status == "Completed":
                completed_tasks.append(task_name)
            elif task.status == "In Progress":
                ongoing_tasks.append(task_name)
            else:
                delayed_tasks.append(task_name)

        print("Completed Tasks:", completed_tasks)
        print("Ongoing Tasks:", ongoing_tasks)
        print("Delayed Tasks:", delayed_tasks)


# Example Usage
if __name__ == "__main__":
    task_chain = TaskChain()

    task_a = task_chain.create_task("Task A")
    task_b = task_chain.create_task("Task B")
    task_c = task_chain.create_task("Task C")

    task_b.add_dependency(task_a)
    task_c.add_dependency(task_b)

    task_chain.mark_task_as_started("Task A", "2022-10-10 08:00:00")
    task_chain.mark_task_as_completed("Task A", "2022-10-10 10:00:00")

    task_chain.mark_task_as_started("Task B", "2022-10-10 10:30:00")
    task_chain.mark_task_as_completed("Task B", "2022-10-10 12:00:00")

    task_chain.generate_report()
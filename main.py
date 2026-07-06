from datetime import date
from pawpal_system import Owner, Pet, Task, Scheduler


today = date.today().isoformat()

owner = Owner("Robby", "robby@example.com")

dog = Pet("Buddy", "Dog", 5)
cat = Pet("Mittens", "Cat", 3)

owner.add_pet(dog)
owner.add_pet(cat)

scheduler = Scheduler()

scheduler.add_task(Task("Evening medicine", "Medication", today, "18:00", 1, "daily"), cat)
scheduler.add_task(Task("Morning walk", "Exercise", today, "08:00", 1, "daily"), dog)
scheduler.add_task(Task("Breakfast", "Feeding", today, "09:00", 2, "daily"), dog)
scheduler.add_task(Task("Clean litter box", "Cleaning", today, "09:00", 2, "daily"), cat)

print("Today's Schedule - Sorted by Time")
print("---------------------------------")
for task in scheduler.sort_by_time():
    status = "Done" if task.completed else "Pending"
    print(f"{task.due_time} | {task.pet_name}: {task.title} ({task.task_type}) [{status}]")

print("\nBuddy's Tasks")
print("-------------")
for task in scheduler.filter_by_pet("Buddy"):
    print(f"{task.due_time} | {task.title}")

print("\nPending Tasks")
print("-------------")
for task in scheduler.filter_by_status(False):
    print(f"{task.due_time} | {task.pet_name}: {task.title}")

print("\nConflict Warnings")
print("-----------------")
for warning in scheduler.detect_conflicts():
    print(warning)

print("\nRecurring Task Demo")
print("-------------------")
completed_task = scheduler.tasks[0]
next_task = scheduler.mark_task_complete(completed_task)

print(f"Completed: {completed_task.title} on {completed_task.due_date}")
if next_task:
    print(f"Created next task: {next_task.title} on {next_task.due_date}")
from datetime import date
from pawpal_system import Owner, Pet, Task, Scheduler


today = date.today().isoformat()

owner = Owner("Robby", "robby@example.com")

dog = Pet("Buddy", "Dog", 5)
cat = Pet("Mittens", "Cat", 3)

owner.add_pet(dog)
owner.add_pet(cat)

scheduler = Scheduler()

scheduler.add_task(Task("Morning walk", "Exercise", today, "08:00", 1), dog)
scheduler.add_task(Task("Breakfast", "Feeding", today, "09:00", 2), dog)
scheduler.add_task(Task("Clean litter box", "Cleaning", today, "10:30", 2), cat)
scheduler.add_task(Task("Evening medicine", "Medication", today, "18:00", 1), cat)

print("Today's Schedule")
print("----------------")

for task in scheduler.prioritize_tasks():
    if task.is_due_today():
        status = "Done" if task.completed else "Pending"
        print(
            f"{task.due_time} | {task.pet_name}: {task.title} "
            f"({task.task_type}) - Priority {task.priority} [{status}]"
        )
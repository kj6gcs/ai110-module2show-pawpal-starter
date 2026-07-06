"""
PawPal Logic Layer
Classes mirror the UML in diagrams/uml_draft.mmd.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date, timedelta


# ---------------------------------------------------------------------------
# Task — a single care item for a pet
# ---------------------------------------------------------------------------

@dataclass
class Task:
    title: str
    task_type: str
    due_date: str
    due_time: str
    priority: int
    frequency: str = "once"
    completed: bool = False
    pet_name: str = ""

    def __post_init__(self) -> None:
        try:
            date.fromisoformat(self.due_date)
        except ValueError:
            raise ValueError(
                f"due_date must be ISO-8601 (YYYY-MM-DD), got: {self.due_date!r}"
            )

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def is_due_today(self) -> bool:
        """Return True if due_date matches today's date."""
        return self.due_date == date.today().isoformat()


# ---------------------------------------------------------------------------
# Pet — an animal owned by an Owner
# ---------------------------------------------------------------------------

@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a Task to this pet and stamp the pet's name onto the task."""
        task.pet_name = self.name
        self.tasks.append(task)

    def get_tasks(self) -> list[Task]:
        """Return all tasks for this pet."""
        return self.tasks


# ---------------------------------------------------------------------------
# Scheduler — manages and prioritizes tasks across pets
# ---------------------------------------------------------------------------

class Scheduler:
    def __init__(self) -> None:
        self.tasks: list[Task] = []

    def add_task(self, task: Task, pet: Pet) -> None:
        """Register the task with both the pet and scheduler."""
        pet.add_task(task)
        self.tasks.append(task)

    def get_today_tasks(self) -> list[Task]:
        """Return all tasks that are due today."""
        return [t for t in self.tasks if t.is_due_today()]

    def prioritize_tasks(self) -> list[Task]:
        """Return tasks sorted by due date, due time, and priority."""
        return sorted(self.tasks, key=lambda t: (t.due_date, t.due_time, t.priority))

    def sort_by_time(self) -> list[Task]:
        """Return tasks sorted by due time."""
        return sorted(self.tasks, key=lambda t: t.due_time)

    def filter_by_pet(self, pet_name: str) -> list[Task]:
        """Return tasks that belong to a specific pet."""
        return [t for t in self.tasks if t.pet_name.lower() == pet_name.lower()]

    def filter_by_status(self, completed: bool) -> list[Task]:
        """Return tasks matching the requested completion status."""
        return [t for t in self.tasks if t.completed == completed]

    def detect_conflicts(self) -> list[str]:
        """Return warning messages for tasks scheduled at the same date and time."""
        warnings = []
        seen = {}

        for task in self.tasks:
            key = (task.due_date, task.due_time)

            if key in seen:
                other = seen[key]
                warnings.append(
                    f"Conflict: {task.pet_name}'s task '{task.title}' "
                    f"overlaps with {other.pet_name}'s task '{other.title}' "
                    f"on {task.due_date} at {task.due_time}."
                )
            else:
                seen[key] = task

        return warnings

    def mark_task_complete(self, task: Task) -> Task | None:
        """Mark a task complete and create the next recurring task if needed."""
        task.mark_complete()

        if task.frequency.lower() == "daily":
            next_date = date.fromisoformat(task.due_date) + timedelta(days=1)
        elif task.frequency.lower() == "weekly":
            next_date = date.fromisoformat(task.due_date) + timedelta(weeks=1)
        else:
            return None

        next_task = Task(
            title=task.title,
            task_type=task.task_type,
            due_date=next_date.isoformat(),
            due_time=task.due_time,
            priority=task.priority,
            frequency=task.frequency,
            pet_name=task.pet_name,
        )

        self.tasks.append(next_task)
        return next_task

    @classmethod
    def build_from_owner(cls, owner: Owner) -> Scheduler:
        """Construct a Scheduler pre-loaded with every task from an owner's pets."""
        scheduler = cls()
        for pet in owner.get_pets():
            for task in pet.get_tasks():
                scheduler.tasks.append(task)
        return scheduler


# ---------------------------------------------------------------------------
# Owner — a person responsible for one or more pets
# ---------------------------------------------------------------------------

class Owner:
    def __init__(self, name: str, email: str) -> None:
        self.name: str = name
        self.email: str = email
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Register a pet under this owner."""
        self.pets.append(pet)

    def remove_pet(self, pet_name: str) -> None:
        """Remove a pet by name (first match)."""
        self.pets = [p for p in self.pets if p.name != pet_name]

    def get_pets(self) -> list[Pet]:
        """Return all pets owned by this owner."""
        return self.pets

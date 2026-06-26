"""
PawPal Logic Layer
Classes mirror the UML in diagrams/uml_draft.mmd.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date


# ---------------------------------------------------------------------------
# Task — a single care item for a pet
# ---------------------------------------------------------------------------

@dataclass
class Task:
    title: str
    task_type: str
    due_date: str       # must be ISO-8601, e.g. "2026-06-25"
    priority: int       # 1 = highest urgency; lower number = scheduled first
    completed: bool = False
    pet_name: str = ""  # stamped by Pet.add_task(); identifies which pet this belongs to

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
        """Single entry point: registers the task with the pet AND the scheduler.

        Calling this instead of pet.add_task() directly keeps both task lists
        in sync and ensures every task carries a pet_name back-reference.
        """
        pet.add_task(task)       # stamps pet_name, appends to pet.tasks
        self.tasks.append(task)  # keeps scheduler's list current

    def get_today_tasks(self) -> list[Task]:
        """Return all tasks that are due today."""
        return [t for t in self.tasks if t.is_due_today()]

    def prioritize_tasks(self) -> list[Task]:
        """Return tasks sorted ascending by priority (1 = most urgent)."""
        return sorted(self.tasks, key=lambda t: t.priority)

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

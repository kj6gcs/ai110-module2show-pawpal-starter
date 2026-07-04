import pytest
from datetime import date
from pawpal_system import Task, Pet, Owner, Scheduler


def test_task_completion():
    today = date.today().isoformat()
    task = Task("Feed pet", "Feeding", today, "08:00", 2)

    task.mark_complete()

    assert task.completed is True


def test_task_addition_to_pet():
    today = date.today().isoformat()
    pet = Pet("Buddy", "Dog", 5)
    task = Task("Morning walk", "Exercise", today, "08:00", 1)

    pet.add_task(task)

    assert len(pet.tasks) == 1
    assert pet.tasks[0].pet_name == "Buddy"


def test_owner_add_pet():
    owner = Owner("Robby", "robby@example.com")
    pet = Pet("Mittens", "Cat", 3)

    owner.add_pet(pet)

    assert len(owner.get_pets()) == 1
    assert owner.get_pets()[0].name == "Mittens"


def test_scheduler_add_task_to_pet_and_scheduler():
    today = date.today().isoformat()
    scheduler = Scheduler()
    pet = Pet("Buddy", "Dog", 5)
    task = Task("Morning walk", "Exercise", today, "08:00", 1)

    scheduler.add_task(task, pet)

    assert len(pet.get_tasks()) == 1
    assert len(scheduler.tasks) == 1
    assert scheduler.tasks[0].pet_name == "Buddy"


def test_scheduler_get_today_tasks():
    today = date.today().isoformat()
    scheduler = Scheduler()
    pet = Pet("Mittens", "Cat", 3)
    task = Task("Give medicine", "Medication", today, "18:00", 1)

    scheduler.add_task(task, pet)

    today_tasks = scheduler.get_today_tasks()

    assert len(today_tasks) == 1
    assert today_tasks[0].title == "Give medicine"


def test_scheduler_prioritizes_tasks():
    today = date.today().isoformat()
    scheduler = Scheduler()
    pet = Pet("Buddy", "Dog", 5)

    low_priority = Task("Brush fur", "Grooming", today, "12:00", 3)
    high_priority = Task("Give medicine", "Medication", today, "08:00", 1)

    scheduler.add_task(low_priority, pet)
    scheduler.add_task(high_priority, pet)

    prioritized = scheduler.prioritize_tasks()

    assert prioritized[0].title == "Give medicine"
    assert prioritized[1].title == "Brush fur"

def test_invalid_due_date_raises_value_error():
    with pytest.raises(ValueError):
        Task("Bad date", "Test", "07-04-2026", "08:00", 1)


def test_scheduler_build_from_owner():
    today = date.today().isoformat()

    owner = Owner("Robby", "robby@example.com")
    pet = Pet("Mittens", "Cat", 3)
    task = Task("Clean litter box", "Cleaning", today, "10:30", 2)

    pet.add_task(task)
    owner.add_pet(pet)

    scheduler = Scheduler.build_from_owner(owner)

    assert len(scheduler.tasks) == 1
    assert scheduler.tasks[0].title == "Clean litter box"
    assert scheduler.tasks[0].pet_name == "Mittens"


def test_owner_remove_pet():
    owner = Owner("Robby", "robby@example.com")
    pet = Pet("Buddy", "Dog", 5)

    owner.add_pet(pet)
    owner.remove_pet("Buddy")

    assert len(owner.get_pets()) == 0
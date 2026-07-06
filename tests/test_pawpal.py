import pytest
from datetime import date, timedelta
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

def test_sort_by_time_returns_chronological_order():
    today = date.today().isoformat()
    pet = Pet("Buddy", "Dog", 5)
    scheduler = Scheduler()

    scheduler.add_task(Task("Dinner", "Feeding", today, "18:00", 2), pet)
    scheduler.add_task(Task("Walk", "Exercise", today, "08:00", 1), pet)
    scheduler.add_task(Task("Brush", "Grooming", today, "12:00", 3), pet)

    sorted_tasks = scheduler.sort_by_time()

    assert [task.due_time for task in sorted_tasks] == ["08:00", "12:00", "18:00"]


def test_daily_recurring_task_creates_next_day_task():
    today = date.today()
    pet = Pet("Mittens", "Cat", 3)
    scheduler = Scheduler()

    task = Task("Give medicine", "Medication", today.isoformat(), "08:00", 1, "daily")
    scheduler.add_task(task, pet)

    next_task = scheduler.mark_task_complete(task)

    assert task.completed is True
    assert next_task is not None
    assert next_task.due_date == (today + timedelta(days=1)).isoformat()
    assert next_task.title == "Give medicine"


def test_weekly_recurring_task_creates_next_week_task():
    today = date.today()
    pet = Pet("Buddy", "Dog", 5)
    scheduler = Scheduler()

    task = Task("Bath", "Grooming", today.isoformat(), "10:00", 2, "weekly")
    scheduler.add_task(task, pet)

    next_task = scheduler.mark_task_complete(task)

    assert next_task is not None
    assert next_task.due_date == (today + timedelta(weeks=1)).isoformat()


def test_once_task_does_not_create_recurring_task():
    today = date.today().isoformat()
    pet = Pet("Buddy", "Dog", 5)
    scheduler = Scheduler()

    task = Task("Vet appointment", "Appointment", today, "14:00", 1, "once")
    scheduler.add_task(task, pet)

    next_task = scheduler.mark_task_complete(task)

    assert task.completed is True
    assert next_task is None


def test_conflict_detection_flags_duplicate_times():
    today = date.today().isoformat()
    scheduler = Scheduler()
    dog = Pet("Buddy", "Dog", 5)
    cat = Pet("Mittens", "Cat", 3)

    scheduler.add_task(Task("Breakfast", "Feeding", today, "09:00", 2), dog)
    scheduler.add_task(Task("Clean litter box", "Cleaning", today, "09:00", 2), cat)

    conflicts = scheduler.detect_conflicts()

    assert len(conflicts) == 1
    assert "Conflict" in conflicts[0]
    assert "09:00" in conflicts[0]


def test_filter_by_pet_returns_only_matching_pet_tasks():
    today = date.today().isoformat()
    scheduler = Scheduler()
    dog = Pet("Buddy", "Dog", 5)
    cat = Pet("Mittens", "Cat", 3)

    scheduler.add_task(Task("Walk", "Exercise", today, "08:00", 1), dog)
    scheduler.add_task(Task("Medicine", "Medication", today, "18:00", 1), cat)

    buddy_tasks = scheduler.filter_by_pet("Buddy")

    assert len(buddy_tasks) == 1
    assert buddy_tasks[0].pet_name == "Buddy"


def test_filter_by_status_returns_only_pending_tasks():
    today = date.today().isoformat()
    scheduler = Scheduler()
    pet = Pet("Buddy", "Dog", 5)

    done_task = Task("Walk", "Exercise", today, "08:00", 1)
    pending_task = Task("Dinner", "Feeding", today, "18:00", 2)

    scheduler.add_task(done_task, pet)
    scheduler.add_task(pending_task, pet)

    done_task.mark_complete()

    pending_tasks = scheduler.filter_by_status(False)

    assert len(pending_tasks) == 1
    assert pending_tasks[0].title == "Dinner"
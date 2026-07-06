# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## ✨ Features

- Manage owner and pet information
- Schedule pet care tasks with priorities and recurrence
- Automatically sort daily schedules chronologically
- Filter tasks by pet and completion status
- Detect scheduling conflicts
- Support daily and weekly recurring tasks
- Streamlit-based user interface
- Automated unit tests with 100% code coverage

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
Today's Schedule
----------------
08:00 | Buddy: Morning walk (Exercise) - Priority 1 [Pending]
09:00 | Buddy: Breakfast (Feeding) - Priority 2 [Pending]
10:30 | Mittens: Clean litter box (Cleaning) - Priority 2 [Pending]
18:00 | Mittens: Evening medicine (Medication) - Priority 1 [Pending]
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:

python -m pytest
============================================================================= test session starts ==============================================================================
platform win32 -- Python 3.13.3, pytest-9.1.1, pluggy-1.6.0
rootdir: D:\0000 Codepath\AI110 - Foundations of AI Engineering\ai110-module2show-pawpal-starter
plugins: anyio-4.14.1
collected 6 items

tests\test_pawpal.py ......                                                                                                                                                                                         [100%]
============================================================================== 6 passed in 0.10s ===============================================================================

# Run with coverage:

python -m pytest --cov=pawpal_system
============================================================================== test session starts ===============================================================================
platform win32 -- Python 3.13.3, pytest-9.1.1, pluggy-1.6.0
rootdir: D:\0000 Codepath\AI110 - Foundations of AI Engineering\ai110-module2show-pawpal-starter
plugins: anyio-4.14.1, cov-7.1.0
collected 9 items

tests\test_pawpal.py .........                                                                                                                                                                                      [100%]

================================================================================= tests coverage =================================================================================
____________________________________________________________________________________ coverage: platform win32, python 3.13.3-final-0 _____________________________________________________________________________________

Name               Stmts   Miss  Cover
--------------------------------------
pawpal_system.py      60      0   100%
--------------------------------------
TOTAL                 60      0   100%
=============================================================================== 9 passed in 0.08s ================================================================================
```

### Updated Automated Tests (end of Phase 5) Results

```
============================================================================== test session starts ==============================================================================
platform win32 -- Python 3.13.3, pytest-9.0.3, pluggy-1.6.0
rootdir: D:\0000 Codepath\AI110 - Foundations of AI Engineering\ai110-module2show-pawpal-starter
plugins: anyio-4.13.0
collected 16 items

tests\test_pawpal.py ................                                                                                                                                                              [100%]

============================================================================== 16 passed in 0.07s ===============================================================================
```

## 📐 Smarter Scheduling

| Feature            | Method(s)                                                      | Notes                                                            |
| ------------------ | -------------------------------------------------------------- | ---------------------------------------------------------------- |
| Task sorting       | `Scheduler.sort_by_time()` and `Scheduler.prioritize_tasks()`  | Sorts tasks by scheduled time or by date, time, and priority     |
| Filtering          | `Scheduler.filter_by_pet()` and `Scheduler.filter_by_status()` | Filters tasks by pet name or completion status                   |
| Conflict detection | `Scheduler.detect_conflicts()`                                 | Returns warning messages when tasks share the same date and time |
| Recurring tasks    | `Scheduler.mark_task_complete()`                               | Marks a task complete and creates the next daily or weekly task  |

## 📸 Demo Walkthrough

1. The user opens the PawPal+ Streamlit app.
2. The user enters or updates their owner profile.
3. The user adds one or more pets.
4. The user schedules tasks for each pet, including task type, due date, due time, priority, and frequency.
5. The app stores the owner, pets, tasks, and scheduler in `st.session_state` so data persists during the session.
6. The schedule view displays today’s tasks in chronological order.
7. If two tasks are scheduled for the same date and time, the app displays a warning instead of crashing.
8. The backend can also mark recurring tasks complete and create the next daily or weekly occurrence.

**Screenshot or video** _(optional)_:

<p align="center">
  <a href="https://youtu.be/NUvS6ufa0jA">
    <img src="https://img.youtube.com/vi/NUvS6ufa0jA/maxresdefault.jpg" width="800" alt="PawPal+ Demo">
  </a>
</p>

<p align="center">
  ▶️ Click the thumbnail above to watch the full demonstration on YouTube.
</p>

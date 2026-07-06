# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

For the design, I chose four main classes: Owner, Pet, Task, and Scheduler. The Owner class stores information about the pet owner and keeps track of their pets. The Pet class represents each animal and stores basic information like name, species, age, and related care tasks. The Task class represents things the owner needs to do, such as feedings, walks, medications, or appointments. The Scheduler class manages task organization by finding today’s tasks and sorting tasks by priority. It is worth noting that Pet and Scheduler serve different scopes rather than duplicating responsibility: Pet owns the task list for a single animal, while Scheduler provides a cross-pet view used for day-level scheduling. This structure keeps the system modular because each class has a clear responsibility.

#### Core Actions:

1. Add an owner & their pets
2. Create / schedule pet care tasks (feeding, walks, meds, appointments, etc.)
3. View the day's (prioritized) tasks.

**b. Design changes**

Yes, several refinements were made after reviewing the initial skeleton against the UML.

The most significant change was making `Scheduler.add_task()` the single entry point for registering a task. In the original skeleton, `Pet.add_task()` and `Scheduler.add_task()` were independent, meaning a caller could add a task to a pet without the Scheduler ever knowing about it. The fix was to have `Scheduler.add_task(task, pet)` call `pet.add_task()` internally, so both lists are always updated together.

A related change was adding a `pet_name` field to the `Task` dataclass. Because tasks were only stored in flat lists, there was no way to tell which pet a task belonged to when the Scheduler returned results. Stamping `pet_name` onto the task inside `Pet.add_task()` solves this without requiring a full object back-reference.

A `Scheduler.build_from_owner()` class method was also added. The original design had no connection between an Owner and a Scheduler, making it impossible to bootstrap the Scheduler from an existing owner's pet data. This method bridges that gap.

Finally, two smaller robustness fixes were made: a `__post_init__` validator on `Task` that rejects non-ISO-8601 date strings immediately rather than silently returning wrong results later, and an inline comment on `prioritize_tasks()` documenting that priority 1 means most urgent, so the ascending sort is intentional.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

My scheduler considers several constraints when organizing tasks. It uses the task's due date to determine whether it belongs in today's schedule, sorts tasks chronologically by their scheduled time, and then uses task priority to determine the order of tasks that occur around the same time. The scheduler also keeps track of the pet associated with each task so tasks can be filtered by pet, and it supports recurring daily and weekly tasks by automatically creating the next occurrence when a recurring task is completed.

I chose these constraints because they represent the information a pet owner is most likely to care about when planning their day. Knowing when a task needs to happen is more important than simply knowing how urgent it is, so time is considered first, with priority used to organize tasks that occur during the same part of the day.

**b. Tradeoffs**

One tradeoff my scheduler makes is that conflict detection only checks for tasks scheduled at the exact same date and time. It does not consider task duration or detect partially overlapping appointments.

This tradeoff keeps the scheduling algorithm simple, easy to understand, and efficient while still providing useful warnings for the most obvious conflicts. A more sophisticated scheduling algorithm could compare task durations and overlapping time windows, but that would add complexity beyond the scope of this project.

---

## 3. AI Collaboration

**a. How you used AI**

I used AI throughout the project as a development assistant rather than as a code generator. AI helped brainstorm the initial class design, review my UML, suggest improvements to my class relationships, generate starter implementations, explain Python features such as `dataclasses`, lambda expressions, and `st.session_state`, and help create and debug automated tests. I also used AI to review documentation and provide suggestions for improving readability and organization.

The most helpful prompts were those that focused on a specific problem instead of asking AI to solve the entire project. Questions such as "How should the Scheduler retrieve all tasks from the Owner's pets?" or "Why is this test failing?" produced much more useful results than broad requests for complete implementations.

**b. Judgment and verification**

One example where I did not accept an AI suggestion as-is was during the Scheduler implementation. An early suggestion simplified the relationships between the classes, but it removed some of the separation of responsibilities that I wanted between the Owner, Pet, and Scheduler classes. Instead of replacing my design, I adapted the suggestion by making Scheduler.add_task() the single entry point while preserving the overall architecture.

I evaluated AI suggestions by comparing them against my UML, running the application, executing the automated test suite, and verifying that each change actually improved the project without introducing regressions.

---

## 4. Testing and Verification

**a. What you tested**

The automated test suite verifies the core behaviors of the application, including task completion, adding tasks to pets, owner management, scheduler registration, retrieving today's tasks, task prioritization, chronological sorting, filtering by pet, filtering by completion status, recurring daily and weekly tasks, one-time task behavior, conflict detection, and invalid date validation.

These tests were important because they verify both the individual classes and the scheduling algorithms. They also helped ensure that adding new features during later phases did not accidentally break functionality that was already working.

**b. Confidence**

I am very confident in the reliability of the current implementation. The project includes sixteen automated unit tests, all of which pass successfully, and the backend achieved 100% code coverage using `pytest-cov`. While code coverage does not guarantee the absence of bugs, it provides confidence that every executable path in the current implementation has been exercised.

If I continued developing this project, I would add tests for overlapping task durations, deleting or editing tasks after creation, multiple owners with separate accounts, recurring tasks over long periods of time, and additional edge cases involving invalid user input.

---

## 5. Reflection

**a. What went well**

I am most satisfied with how the object-oriented design evolved throughout the project. The responsibilities of each class remained well separated while still working together as a complete system. I was also pleased with the automated testing, which grew from a few basic tests into a comprehensive suite with sixteen passing tests and 100% code coverage.

**b. What you would improve**

With another iteration, I would expand the scheduling algorithm to consider task duration instead of only scheduled times. I would also redesign the application to support multiple owner accounts, persistent data storage, and editing or deleting existing tasks through the Streamlit interface. Those additions would make the application much closer to a production-ready pet management system.

**c. Key takeaway**

The biggest lesson I learned is that AI is most effective when treated as a collaborator rather than an autopilot. AI can quickly generate ideas, explain unfamiliar concepts, and help debug problems, but it still requires human oversight to make architectural decisions, evaluate tradeoffs, and verify correctness. Acting as the lead architect throughout the project reinforced the importance of understanding the system well enough to decide when to accept, modify, or reject AI-generated suggestions.

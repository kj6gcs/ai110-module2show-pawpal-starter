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

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

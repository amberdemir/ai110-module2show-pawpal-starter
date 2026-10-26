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

```
Today's Schedule
==============================================================
Time   Task            Pet       Duration  Priority
--------------------------------------------------------------
07:30  Morning walk    Biscuit   30 min    high
08:00  Feeding         Mochi     10 min    high
18:00  Play session    Mochi     20 min    medium

Amber has 75 minutes today. Tasks were picked by priority (high first), shortest first within a priority, until the time ran out.
Planned 3 task(s) using 60 min (15 min left).
  + Morning walk for Biscuit (high, 30 min): fit in the time.
  + Feeding for Mochi (high, 10 min): fit in the time.
  + Play session for Mochi (medium, 20 min): fit in the time.
  - Grooming for Biscuit (low, 45 min): skipped, it needs more than the 15 min left.
```

## Implementation Summary

PawPal+ is built from four classes in `pawpal_system.py`. An `Owner` holds multiple `Pet`s, and each `Pet` holds its own list of `Task`s. Each `Task` has a title, duration, priority, start time, frequency, and completion status. The `Scheduler` gets every task through `Owner.get_all_tasks()`, skips completed ones, sorts by priority and then duration, and fills the owner's available minutes greedily. Tasks that don't fit go in a skipped list. The final plan is sorted by time, and `explain_plan()` says why each task was picked or skipped. `main.py` is a terminal demo, and `tests/test_pawpal.py` checks task completion and task addition.

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
python -m pytest
```

Sample test output:

The tests cover:
- Sorting tasks by time, including tasks added out of order
- Recurring tasks (daily and weekly create the next task, "once" tasks don't, completing twice doesn't duplicate)
- Conflict detection for tasks at the same time, and no warning for different times
- Filtering by pet and completion status
- Edge cases: a pet with no tasks, completed tasks left out of the plan, and tasks that don't fit going to skipped

Sample test output:

```
tests/test_pawpal.py .................                                               [100%]

==================================== 17 passed in 0.03s ====================================
```

Confidence level: ★★★★☆ (4/5). The tests cover the main behaviors and several edge cases. Next I'd test overlapping durations, since the conflict check only catches exact time matches.



```
tests/test_pawpal.py::test_mark_complete_changes_status PASSED           [ 50%]
tests/test_pawpal.py::test_add_task_increases_pet_task_count PASSED      [100%]
2 passed in 0.02s
```

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Sorts "HH:MM" strings with `sorted()` and a lambda key |
| Filtering | `Scheduler.filter_tasks()` | Filters by pet name and/or completion status |
| Conflict handling | `Scheduler.detect_conflicts()` | Returns warnings for incomplete tasks at the same date and time; conflicting tasks still get scheduled |
| Recurring tasks | `Scheduler.mark_task_complete()` | Daily and weekly tasks create a new task due 1 or 7 days later; "once" tasks don't repeat |



##  Features

- **Priority-based planning:** `Scheduler.generate_plan()` fills the owner's available minutes with high-priority tasks first (shortest first within a priority), skips tasks that don't fit, and orders the final plan by start time
- **Sorting by time:** `Scheduler.sort_by_time()` orders tasks by their "HH:MM" start time
- **Filtering:** `Scheduler.filter_tasks()` filters tasks by pet and/or completion status
- **Conflict warnings:** `Scheduler.detect_conflicts()` warns when incomplete tasks share the same date and time, for the same pet or different pets
- **Recurring tasks:** `Scheduler.mark_task_complete()` completes a task and, for daily or weekly tasks, adds the next one due 1 or 7 days later ("once" tasks don't repeat)
- **Plan explanations:** `Scheduler.explain_plan()` explains why each task was picked or skipped

## 📸 Demo Walkthrough

The Streamlit app (`streamlit run app.py`) lets you set the owner's name and available minutes, add pets, and add tasks with a duration, priority, frequency, and start time. A **Task List** shows every task sorted by time, with filters for pet and completion status and a control to mark a task complete. **Build Schedule** generates today's plan as a table, shows a warning for each scheduling conflict, and explains which tasks were picked or skipped.

Example workflow:

1. Enter the owner's name and available minutes at the top of the page (for example, Jordan with 90 minutes).
2. Under **Pets**, type "Biscuit", choose "dog", and click **Add pet**. Add a second pet, "Mochi" (cat), the same way.
3. Under **Tasks**, add a few tasks with different start times, such as "Morning walk" for Biscuit at 07:30 (high, daily), "Feeding" for Mochi at 12:00 (high, daily), and "Grooming" for Biscuit at 16:00 (low, weekly).
4. Click **Generate schedule**. A success message shows how many tasks were planned and how many minutes they use, followed by today's schedule sorted by time and an explanation of the plan.
5. Add two tasks at the same start time, for example "Breakfast" for Biscuit and "Play session" for Mochi, both at 08:00. The schedule now shows a warning naming both tasks and the time, with a suggestion to change one start time.
6. In the **Task List**, choose Biscuit's daily "Morning walk" under **Mark a task complete** and click **Mark complete**. A success message confirms the next walk was added for tomorrow, and the new task appears in the list with tomorrow's due date. It stays out of today's schedule.

This walkthrough shows priority-based planning, sorting by time, filtering by pet and status, conflict detection, daily recurrence, and plan explanations.

**Sample CLI output (`python main.py`):**

```
All tasks (in the order they were added)
----------------------------------------------------------------------
  16:00  Grooming        Biscuit   45 min   low     weekly  2026-10-25  todo
  07:30  Morning walk    Biscuit   30 min   high    daily   2026-10-25  todo
  08:00  Breakfast       Biscuit   5 min    high    daily   2026-10-25  todo
  18:00  Play session    Mochi     20 min   medium  daily   2026-10-25  todo
  08:00  Feeding         Mochi     10 min   high    daily   2026-10-25  todo
  11:00  Vet visit       Mochi     60 min   medium  once    2026-10-25  todo

Sorted by time
----------------------------------------------------------------------
  07:30  Morning walk    Biscuit   30 min   high    daily   2026-10-25  todo
  08:00  Breakfast       Biscuit   5 min    high    daily   2026-10-25  todo
  08:00  Feeding         Mochi     10 min   high    daily   2026-10-25  todo
  11:00  Vet visit       Mochi     60 min   medium  once    2026-10-25  todo
  16:00  Grooming        Biscuit   45 min   low     weekly  2026-10-25  todo
  18:00  Play session    Mochi     20 min   medium  daily   2026-10-25  todo

Filtered: Mochi's tasks
----------------------------------------------------------------------
  18:00  Play session    Mochi     20 min   medium  daily   2026-10-25  todo
  08:00  Feeding         Mochi     10 min   high    daily   2026-10-25  todo
  11:00  Vet visit       Mochi     60 min   medium  once    2026-10-25  todo

Completed 'Morning walk' (daily). Next one added for 2026-10-26.

Biscuit's tasks after completing the walk
----------------------------------------------------------------------
  16:00  Grooming        Biscuit   45 min   low     weekly  2026-10-25  todo
  07:30  Morning walk    Biscuit   30 min   high    daily   2026-10-25  done
  08:00  Breakfast       Biscuit   5 min    high    daily   2026-10-25  todo
  07:30  Morning walk    Biscuit   30 min   high    daily   2026-10-26  todo

Filtered: completed tasks
----------------------------------------------------------------------
  07:30  Morning walk    Biscuit   30 min   high    daily   2026-10-25  done

Filtered: incomplete tasks
----------------------------------------------------------------------
  16:00  Grooming        Biscuit   45 min   low     weekly  2026-10-25  todo
  08:00  Breakfast       Biscuit   5 min    high    daily   2026-10-25  todo
  07:30  Morning walk    Biscuit   30 min   high    daily   2026-10-26  todo
  18:00  Play session    Mochi     20 min   medium  daily   2026-10-25  todo
  08:00  Feeding         Mochi     10 min   high    daily   2026-10-25  todo
  11:00  Vet visit       Mochi     60 min   medium  once    2026-10-25  todo

Conflict check
----------------------------------------------------------------------
  WARNING: Conflict on 2026-10-25 at 08:00: Breakfast (Biscuit), Feeding (Mochi)

Today's Schedule
==============================================================
Time   Task            Pet       Duration  Priority
--------------------------------------------------------------
08:00  Breakfast       Biscuit   5 min     high
08:00  Feeding         Mochi     10 min    high
18:00  Play session    Mochi     20 min    medium

Amber has 75 minutes today. Tasks were picked by priority (high first), shortest first within a priority, until the time ran out.
Planned 3 task(s) using 35 min (40 min left).
  + Breakfast for Biscuit (high, 5 min): fit in the time.
  + Feeding for Mochi (high, 10 min): fit in the time.
  + Play session for Mochi (medium, 20 min): fit in the time.
  - Vet visit for Mochi (medium, 60 min): skipped, it needs more than the 40 min left.
  - Grooming for Biscuit (low, 45 min): skipped, it needs more than the 40 min left.
```

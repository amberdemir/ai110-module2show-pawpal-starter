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

```
tests/test_pawpal.py::test_mark_complete_changes_status PASSED           [ 50%]
tests/test_pawpal.py::test_add_task_increases_pet_task_count PASSED      [100%]
2 passed in 0.02s
```

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | | e.g., by priority, duration |
| Filtering | | e.g., skip tasks if time runs out |
| Conflict handling | | e.g., overlapping time slots |
| Recurring tasks | | e.g., daily vs. weekly |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
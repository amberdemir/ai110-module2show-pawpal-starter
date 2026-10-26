from collections import defaultdict
from dataclasses import dataclass, field, replace
from datetime import date, timedelta

# Lower number = higher priority. Used for sorting and to validate priority strings.
PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str  # "high", "medium", or "low"
    completed: bool = False
    pet_name: str = ""  # set by Pet.add_task()
    time: str = "09:00"  # HH:MM start time
    frequency: str = "daily"  # "once", "daily", or "weekly"
    due_date: date = field(default_factory=date.today)

    def mark_complete(self):
        """Mark this task as done."""
        self.completed = True


@dataclass
class Pet:
    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        """Tag the task with this pet's name and add it to the pet's tasks."""
        task.pet_name = self.name
        self.tasks.append(task)

    def get_tasks(self) -> list[Task]:
        """Return all tasks for this pet."""
        return self.tasks


@dataclass
class Owner:
    name: str
    available_minutes: int
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet):
        """Add a pet to this owner."""
        self.pets.append(pet)

    def get_all_tasks(self) -> list[Task]:
        """Collect tasks from all of the owner's pets."""
        return [task for pet in self.pets for task in pet.get_tasks()]


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner
        self.plan: list[Task] = []
        self.skipped: list[Task] = []
        self._planned = False

    def generate_plan(self) -> list[Task]:
        """Fill the owner's time with incomplete tasks by priority, then order them by time."""
        self.plan = []
        self.skipped = []
        remaining = self.owner.available_minutes

        # Only today's (or overdue) tasks; next occurrences of recurring tasks wait for their day.
        pending = [
            t for t in self.owner.get_all_tasks() if not t.completed and t.due_date <= date.today()
        ]
        pending.sort(key=lambda t: (PRIORITY_ORDER[t.priority], t.duration_minutes))

        for task in pending:
            if task.duration_minutes <= remaining:
                self.plan.append(task)
                remaining -= task.duration_minutes
            else:
                self.skipped.append(task)

        self.plan = self.sort_by_time(self.plan)
        self._planned = True
        return self.plan

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        """Return the tasks sorted by their HH:MM start time."""
        return sorted(tasks, key=lambda t: t.time)

    def filter_tasks(self, pet_name: str | None = None, completed: bool | None = None) -> list[Task]:
        """Return the owner's tasks, optionally limited to one pet and/or a completion status."""
        tasks = self.owner.get_all_tasks()
        if pet_name is not None:
            tasks = [t for t in tasks if t.pet_name == pet_name]
        if completed is not None:
            tasks = [t for t in tasks if t.completed == completed]
        return tasks

    def mark_task_complete(self, task: Task) -> Task | None:
        """Complete a task and, if it repeats, add its next occurrence to the same pet."""
        if task.completed:
            return None  # already done; don't create a second copy
        task.mark_complete()

        if task.frequency == "daily":
            gap = timedelta(days=1)
        elif task.frequency == "weekly":
            gap = timedelta(days=7)
        else:
            return None  # "once" tasks don't repeat

        pet = next((p for p in self.owner.pets if p.name == task.pet_name), None)
        if pet is None:
            raise ValueError(f"No pet named {task.pet_name!r} for task {task.title!r}")
        next_task = replace(task, completed=False, due_date=task.due_date + gap)
        pet.add_task(next_task)
        return next_task

    def detect_conflicts(self) -> list[str]:
        """Return a warning for each date and time that has two or more incomplete tasks."""
        slots = defaultdict(list)
        for t in self.filter_tasks(completed=False):
            slots[(t.due_date, t.time)].append(t)

        warnings = []
        for (day, time), tasks in sorted(slots.items()):
            if len(tasks) > 1:
                names = ", ".join(f"{t.title} ({t.pet_name})" for t in tasks)
                warnings.append(f"Conflict on {day} at {time}: {names}")
        return warnings

    def explain_plan(self) -> str:
        """Explain which tasks were picked, which were skipped, and why."""
        if not self._planned:
            return "No plan yet. Run generate_plan() first."

        available = self.owner.available_minutes
        used = sum(t.duration_minutes for t in self.plan)
        left = available - used
        lines = [
            f"{self.owner.name} has {available} minutes today. "
            f"Tasks were picked by priority (high first), shortest first within a priority, "
            f"until the time ran out.",
            f"Planned {len(self.plan)} task(s) using {used} min ({left} min left).",
        ]
        for t in self.plan:
            lines.append(f"  + {t.title} for {t.pet_name} ({t.priority}, {t.duration_minutes} min): fit in the time.")
        for t in self.skipped:
            lines.append(
                f"  - {t.title} for {t.pet_name} ({t.priority}, {t.duration_minutes} min): "
                f"skipped, it needs more than the {left} min left."
            )
        if not self.skipped:
            lines.append("Nothing was skipped.")
        return "\n".join(lines)

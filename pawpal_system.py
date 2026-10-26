from dataclasses import dataclass, field

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

        pending = [t for t in self.owner.get_all_tasks() if not t.completed]
        pending.sort(key=lambda t: (PRIORITY_ORDER[t.priority], t.duration_minutes))

        for task in pending:
            if task.duration_minutes <= remaining:
                self.plan.append(task)
                remaining -= task.duration_minutes
            else:
                self.skipped.append(task)

        self.plan.sort(key=lambda t: t.time)
        self._planned = True
        return self.plan

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

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

    def mark_complete(self):
        """Mark this task as done."""
        pass


@dataclass
class Pet:
    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        """Add a care task to this pet and set the task's pet_name."""
        pass

    def get_tasks(self) -> list[Task]:
        """Return all tasks for this pet."""
        pass


@dataclass
class Owner:
    name: str
    available_minutes: int
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet):
        """Add a pet to this owner."""
        pass

    def get_all_tasks(self) -> list[Task]:
        """Collect tasks from all of the owner's pets."""
        pass


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner
        self.plan: list[Task] = []
        self.skipped: list[Task] = []

    def generate_plan(self) -> list[Task]:
        """Pick and order tasks to fit the owner's available time.

        Resets self.plan and self.skipped, then sorts incomplete tasks by
        (priority, duration) so shorter tasks win ties. Fills greedily:
        tasks that fit go in self.plan, the rest go in self.skipped.
        Completed tasks are left out of both lists.
        """
        pass

    def explain_plan(self) -> str:
        """Explain why tasks were chosen or skipped, using self.plan and self.skipped.

        Returns a "no plan yet" message if generate_plan() hasn't been run.
        """
        pass

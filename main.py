from pawpal_system import Owner, Pet, Scheduler, Task


def print_tasks(title, tasks):
    """Print a heading and one line per task."""
    print(title)
    print("-" * 70)
    if not tasks:
        print("  (none)")
    for t in tasks:
        status = "done" if t.completed else "todo"
        print(
            f"  {t.time:<7}{t.title:<16}{t.pet_name:<10}{str(t.duration_minutes) + ' min':<9}"
            f"{t.priority:<8}{t.frequency:<8}{t.due_date}  {status}"
        )
    print()


def main():
    owner = Owner("Amber", available_minutes=75)

    biscuit = Pet("Biscuit", "dog")
    mochi = Pet("Mochi", "cat")
    owner.add_pet(biscuit)
    owner.add_pet(mochi)

    # Added out of time order on purpose; Breakfast and Feeding share 08:00 to show a conflict.
    mochi.add_task(Task("Play session", 20, "medium", time="18:00"))
    biscuit.add_task(Task("Grooming", 45, "low", time="16:00", frequency="weekly"))
    biscuit.add_task(Task("Morning walk", 30, "high", time="07:30"))
    mochi.add_task(Task("Feeding", 10, "high", time="08:00"))
    biscuit.add_task(Task("Breakfast", 5, "high", time="08:00"))
    mochi.add_task(Task("Vet visit", 60, "medium", time="11:00", frequency="once"))

    scheduler = Scheduler(owner)

    print_tasks("All tasks (in the order they were added)", owner.get_all_tasks())
    print_tasks("Sorted by time", scheduler.sort_by_time(owner.get_all_tasks()))
    print_tasks("Filtered: Mochi's tasks", scheduler.filter_tasks(pet_name="Mochi"))

    walk = next(t for t in biscuit.get_tasks() if t.title == "Morning walk")
    next_walk = scheduler.mark_task_complete(walk)
    print(f"Completed '{walk.title}' (daily). Next one added for {next_walk.due_date}.\n")

    print_tasks("Biscuit's tasks after completing the walk", scheduler.filter_tasks(pet_name="Biscuit"))
    print_tasks("Filtered: completed tasks", scheduler.filter_tasks(completed=True))
    print_tasks("Filtered: incomplete tasks", scheduler.filter_tasks(completed=False))

    print("Conflict check")
    print("-" * 70)
    for warning in scheduler.detect_conflicts() or ["  No conflicts."]:
        print(f"  WARNING: {warning}")
    print()

    plan = scheduler.generate_plan()
    print("Today's Schedule")
    print("=" * 62)
    print(f"{'Time':<7}{'Task':<16}{'Pet':<10}{'Duration':<10}{'Priority'}")
    print("-" * 62)
    for t in plan:
        print(f"{t.time:<7}{t.title:<16}{t.pet_name:<10}{str(t.duration_minutes) + ' min':<10}{t.priority}")
    print()
    print(scheduler.explain_plan())


if __name__ == "__main__":
    main()

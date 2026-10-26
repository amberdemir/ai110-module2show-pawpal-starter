from datetime import date

from pawpal_system import Owner, Pet, Scheduler, Task


def test_mark_complete_changes_status():
    task = Task("Walk", 30, "high")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet("Biscuit", "dog")
    assert len(pet.get_tasks()) == 0
    pet.add_task(Task("Walk", 30, "high"))
    assert len(pet.get_tasks()) == 1


def make_owner():
    """Build an owner with two pets for the scheduler tests."""
    owner = Owner("Amber", available_minutes=120)
    owner.add_pet(Pet("Biscuit", "dog"))
    owner.add_pet(Pet("Mochi", "cat"))
    return owner


def test_sort_by_time_orders_earliest_first():
    scheduler = Scheduler(make_owner())
    tasks = [Task("C", 10, "low", time="18:00"), Task("A", 10, "low", time="07:30"), Task("B", 10, "low", time="12:00")]
    assert [t.time for t in scheduler.sort_by_time(tasks)] == ["07:30", "12:00", "18:00"]


def test_filter_tasks_by_pet():
    owner = make_owner()
    biscuit, mochi = owner.pets
    biscuit.add_task(Task("Walk", 30, "high"))
    mochi.add_task(Task("Feeding", 10, "high"))
    result = Scheduler(owner).filter_tasks(pet_name="Mochi")
    assert [t.title for t in result] == ["Feeding"]


def test_completing_daily_task_creates_next_day_task():
    owner = make_owner()
    biscuit = owner.pets[0]
    walk = Task("Walk", 30, "high", frequency="daily", due_date=date(2026, 10, 25))
    biscuit.add_task(walk)

    next_walk = Scheduler(owner).mark_task_complete(walk)

    assert walk.completed is True
    assert next_walk.due_date == date(2026, 10, 26)
    assert next_walk.completed is False
    assert next_walk.pet_name == "Biscuit"
    assert len(biscuit.get_tasks()) == 2


def test_detect_conflicts_finds_same_time_pair():
    owner = make_owner()
    biscuit, mochi = owner.pets
    biscuit.add_task(Task("Breakfast", 5, "high", time="08:00"))
    mochi.add_task(Task("Feeding", 10, "high", time="08:00"))
    mochi.add_task(Task("Play", 20, "low", time="18:00"))

    warnings = Scheduler(owner).detect_conflicts()

    assert len(warnings) == 1
    assert "08:00" in warnings[0] and "Breakfast" in warnings[0] and "Feeding" in warnings[0]

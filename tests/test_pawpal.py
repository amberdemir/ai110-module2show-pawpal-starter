from datetime import date

from pawpal_system import Owner, Pet, Scheduler, Task


# mark_complete() flips completed from False to True.
def test_mark_complete_changes_status():
    task = Task("Walk", 30, "high")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


# add_task() adds one task to the pet's list.
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


# sort_by_time() returns tasks earliest first.
def test_sort_by_time_orders_earliest_first():
    scheduler = Scheduler(make_owner())
    tasks = [Task("C", 10, "low", time="18:00"), Task("A", 10, "low", time="07:30"), Task("B", 10, "low", time="12:00")]
    assert [t.time for t in scheduler.sort_by_time(tasks)] == ["07:30", "12:00", "18:00"]


# filter_tasks(pet_name=...) returns only that pet's tasks.
def test_filter_tasks_by_pet():
    owner = make_owner()
    biscuit, mochi = owner.pets
    biscuit.add_task(Task("Walk", 30, "high"))
    mochi.add_task(Task("Feeding", 10, "high"))
    result = Scheduler(owner).filter_tasks(pet_name="Mochi")
    assert [t.title for t in result] == ["Feeding"]


# Completing a daily task adds an incomplete copy due one day later.
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


# Two incomplete tasks at the same date and time produce one warning.
def test_detect_conflicts_finds_same_time_pair():
    owner = make_owner()
    biscuit, mochi = owner.pets
    biscuit.add_task(Task("Breakfast", 5, "high", time="08:00"))
    mochi.add_task(Task("Feeding", 10, "high", time="08:00"))
    mochi.add_task(Task("Play", 20, "low", time="18:00"))

    warnings = Scheduler(owner).detect_conflicts()

    assert len(warnings) == 1
    assert "08:00" in warnings[0] and "Breakfast" in warnings[0] and "Feeding" in warnings[0]


# A pet with no tasks (and an owner with no pets) gives an empty plan without crashing.
def test_pet_with_no_tasks_gives_empty_plan():
    owner = make_owner()
    scheduler = Scheduler(owner)
    assert owner.get_all_tasks() == []
    assert scheduler.generate_plan() == []
    assert scheduler.skipped == []
    assert Scheduler(Owner("Nobody", 60)).generate_plan() == []


# Completing a weekly task adds a copy due exactly 7 days later.
def test_completing_weekly_task_creates_task_seven_days_later():
    owner = make_owner()
    grooming = Task("Grooming", 45, "low", frequency="weekly", due_date=date(2026, 10, 25))
    owner.pets[0].add_task(grooming)

    next_grooming = Scheduler(owner).mark_task_complete(grooming)

    assert next_grooming.due_date == date(2026, 11, 1)
    assert next_grooming.frequency == "weekly"


# Completing a "once" task does not create a new task.
def test_completing_once_task_creates_no_new_task():
    owner = make_owner()
    vet = Task("Vet visit", 60, "medium", frequency="once")
    owner.pets[1].add_task(vet)

    assert Scheduler(owner).mark_task_complete(vet) is None
    assert vet.completed is True
    assert len(owner.pets[1].get_tasks()) == 1


# Completing the same task twice only creates one next copy.
def test_completing_task_twice_creates_only_one_copy():
    owner = make_owner()
    walk = Task("Walk", 30, "high", frequency="daily")
    owner.pets[0].add_task(walk)
    scheduler = Scheduler(owner)

    scheduler.mark_task_complete(walk)
    assert scheduler.mark_task_complete(walk) is None
    assert len(owner.pets[0].get_tasks()) == 2


# Completed tasks are left out of both the plan and the skipped list.
def test_completed_tasks_excluded_from_plan():
    owner = make_owner()
    done = Task("Feeding", 10, "high")
    done.mark_complete()
    owner.pets[0].add_task(done)
    owner.pets[0].add_task(Task("Walk", 30, "high"))

    scheduler = Scheduler(owner)
    plan = scheduler.generate_plan()

    assert [t.title for t in plan] == ["Walk"]
    assert done not in scheduler.skipped


# The next copy of a recurring task (due tomorrow) is not in today's plan.
def test_future_recurring_copy_excluded_from_todays_plan():
    owner = make_owner()
    walk = Task("Walk", 30, "high", frequency="daily")
    owner.pets[0].add_task(walk)
    scheduler = Scheduler(owner)

    next_walk = scheduler.mark_task_complete(walk)

    assert scheduler.generate_plan() == []
    assert next_walk not in scheduler.skipped


# Tasks that don't fit in available_minutes go to skipped, and the plan stays within the limit.
def test_tasks_that_dont_fit_are_skipped():
    owner = Owner("Amber", available_minutes=40)
    pet = Pet("Biscuit", "dog")
    owner.add_pet(pet)
    pet.add_task(Task("Walk", 30, "high"))
    pet.add_task(Task("Grooming", 45, "low"))
    pet.add_task(Task("Play", 20, "medium"))

    scheduler = Scheduler(owner)
    plan = scheduler.generate_plan()

    assert [t.title for t in plan] == ["Walk"]
    assert {t.title for t in scheduler.skipped} == {"Play", "Grooming"}
    assert sum(t.duration_minutes for t in plan) <= owner.available_minutes


# A task that exactly fills the remaining time is planned, not skipped.
def test_task_exactly_filling_time_is_planned():
    owner = Owner("Amber", available_minutes=30)
    pet = Pet("Biscuit", "dog")
    owner.add_pet(pet)
    pet.add_task(Task("Walk", 30, "high"))

    scheduler = Scheduler(owner)

    assert [t.title for t in scheduler.generate_plan()] == ["Walk"]
    assert scheduler.skipped == []


# Tasks at different times produce no conflict warnings.
def test_different_times_produce_no_conflict():
    owner = make_owner()
    owner.pets[0].add_task(Task("Walk", 30, "high", time="07:30"))
    owner.pets[1].add_task(Task("Feeding", 10, "high", time="08:00"))

    assert Scheduler(owner).detect_conflicts() == []


# A completed task at the same time as another task is not a conflict.
def test_completed_task_does_not_cause_conflict():
    owner = make_owner()
    done = Task("Breakfast", 5, "high", time="08:00")
    done.mark_complete()
    owner.pets[0].add_task(done)
    owner.pets[1].add_task(Task("Feeding", 10, "high", time="08:00"))

    assert Scheduler(owner).detect_conflicts() == []


# Tasks added out of order across two pets come out of generate_plan() sorted by time.
def test_plan_sorted_by_time_when_added_out_of_order():
    owner = make_owner()
    biscuit, mochi = owner.pets
    mochi.add_task(Task("Play", 20, "low", time="18:00"))
    biscuit.add_task(Task("Walk", 30, "high", time="07:30"))
    mochi.add_task(Task("Feeding", 10, "medium", time="12:00"))

    plan = Scheduler(owner).generate_plan()

    assert [t.time for t in plan] == ["07:30", "12:00", "18:00"]

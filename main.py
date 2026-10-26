from pawpal_system import Owner, Pet, Scheduler, Task


def main():
    owner = Owner("Amber", available_minutes=75)

    biscuit = Pet("Biscuit", "dog")
    mochi = Pet("Mochi", "cat")
    owner.add_pet(biscuit)
    owner.add_pet(mochi)

    biscuit.add_task(Task("Morning walk", 30, "high", time="07:30"))
    biscuit.add_task(Task("Grooming", 45, "low", time="16:00", frequency="weekly"))
    mochi.add_task(Task("Feeding", 10, "high", time="08:00"))
    mochi.add_task(Task("Play session", 20, "medium", time="18:00"))

    scheduler = Scheduler(owner)
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

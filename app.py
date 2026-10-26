import datetime

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

# One Owner for the whole session; reruns reuse it instead of resetting it.
if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan", available_minutes=90)
owner = st.session_state.owner

st.subheader("Owner")
col1, col2 = st.columns(2)
with col1:
    owner.name = st.text_input("Owner name", value=owner.name)
with col2:
    owner.available_minutes = int(
        st.number_input("Available minutes today", min_value=1, max_value=1440, value=owner.available_minutes)
    )

st.divider()

st.subheader("Pets")
with st.form("add_pet_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        new_pet_name = st.text_input("Pet name")
    with col2:
        new_species = st.selectbox("Species", ["dog", "cat", "other"])
    if st.form_submit_button("Add pet"):
        name = new_pet_name.strip()
        if not name:
            st.error("Please enter a pet name.")
        elif any(p.name.lower() == name.lower() for p in owner.pets):
            st.error(f"You already have a pet named {name}.")
        else:
            owner.add_pet(Pet(name, new_species))
            st.success(f"Added {name}!")

st.divider()

st.subheader("Tasks")
if not owner.pets:
    st.info("Add a pet first, then you can add tasks for it.")
else:
    with st.form("add_task_form"):
        pet_choice = st.selectbox("Pet", [p.name for p in owner.pets])
        task_title = st.text_input("Task title", value="Morning walk")
        col1, col2, col3 = st.columns(3)
        with col1:
            duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        with col2:
            priority = st.selectbox("Priority", ["high", "medium", "low"])
        with col3:
            frequency = st.selectbox("Frequency", ["daily", "weekly", "once"])
        task_time = st.time_input("Start time", value=datetime.time(9, 0))
        if st.form_submit_button("Add task"):
            if not task_title.strip():
                st.error("Please enter a task title.")
            else:
                pet = next(p for p in owner.pets if p.name == pet_choice)
                pet.add_task(
                    Task(
                        title=task_title.strip(),
                        duration_minutes=int(duration),
                        priority=priority,
                        time=task_time.strftime("%H:%M"),
                        frequency=frequency,
                    )
                )
                st.success(f"Added '{task_title.strip()}' for {pet.name}.")

    # Pets at a glance, so pets without tasks still show up.
    st.caption(" · ".join(f"{p.name} ({p.species}): {len(p.get_tasks())} task(s)" for p in owner.pets))

# Fresh Scheduler each rerun; it reads the same session Owner, so it always sees current tasks.
scheduler = Scheduler(owner)

st.divider()

st.subheader("Task List")
# A message saved before st.rerun() so it survives the rerun after marking a task complete.
if "flash" in st.session_state:
    st.success(st.session_state.pop("flash"))

if not owner.get_all_tasks():
    st.info("No tasks yet. Add a task above to see it here.")
else:
    col1, col2 = st.columns(2)
    with col1:
        pet_filter = st.selectbox("Show pet", ["All pets"] + [p.name for p in owner.pets])
    with col2:
        status_filter = st.radio("Show status", ["All", "Not completed", "Completed"], horizontal=True)

    completed = {"All": None, "Not completed": False, "Completed": True}[status_filter]
    filtered = scheduler.filter_tasks(
        pet_name=None if pet_filter == "All pets" else pet_filter, completed=completed
    )
    if filtered:
        st.table(
            [
                {
                    "Time": t.time,
                    "Task": t.title,
                    "Pet": t.pet_name,
                    "Duration (min)": t.duration_minutes,
                    "Priority": t.priority,
                    "Frequency": t.frequency,
                    "Due": str(t.due_date),
                    "Status": "✅ done" if t.completed else "to do",
                }
                for t in scheduler.sort_by_time(filtered)
            ]
        )
    else:
        st.caption("No tasks match this filter.")

    st.markdown("**Mark a task complete**")
    open_tasks = scheduler.sort_by_time(scheduler.filter_tasks(completed=False))
    if not open_tasks:
        st.caption("Everything is done. 🎉")
    else:
        col1, col2 = st.columns([3, 1])
        with col1:
            choice = st.selectbox(
                "Task to complete",
                range(len(open_tasks)),
                format_func=lambda i: f"{open_tasks[i].time} {open_tasks[i].title} "
                f"({open_tasks[i].pet_name}, due {open_tasks[i].due_date})",
                label_visibility="collapsed",
            )
        with col2:
            if st.button("Mark complete"):
                task = open_tasks[choice]
                next_task = scheduler.mark_task_complete(task)
                if next_task:
                    st.session_state.flash = (
                        f"Completed '{task.title}' for {task.pet_name}. "
                        f"It repeats {task.frequency}, so the next one was added for {next_task.due_date}."
                    )
                else:
                    st.session_state.flash = f"Completed '{task.title}' for {task.pet_name}."
                st.rerun()

st.divider()

st.subheader("Build Schedule")
if st.button("Generate schedule"):
    st.session_state.show_plan = True

# Keep showing the schedule after other actions (like marking a task complete) instead of hiding it.
if st.session_state.get("show_plan"):
    if not owner.get_all_tasks():
        st.info("No tasks yet. Add a pet and a task above, then generate a schedule.")
    else:
        plan = scheduler.sort_by_time(scheduler.generate_plan())
        if plan:
            used = sum(t.duration_minutes for t in plan)
            st.success(f"Plan generated: {len(plan)} task(s), {used} of {owner.available_minutes} minutes used.")
            st.markdown("### Today's Schedule")
            st.table(
                [
                    {
                        "Time": t.time,
                        "Task": t.title,
                        "Pet": t.pet_name,
                        "Duration (min)": t.duration_minutes,
                        "Priority": t.priority,
                    }
                    for t in plan
                ]
            )
        else:
            st.info("Nothing left to schedule today. All of today's tasks are done or don't fit.")

        for conflict in scheduler.detect_conflicts():
            st.warning(
                f"⚠️ {conflict}. These tasks start at the same time. "
                f"Try changing the start time of one of them."
            )
        st.text(scheduler.explain_plan())

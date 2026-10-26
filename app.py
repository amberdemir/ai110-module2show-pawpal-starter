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

    for pet in owner.pets:
        st.markdown(f"**{pet.name}** ({pet.species})")
        if pet.get_tasks():
            st.table(
                [
                    {
                        "Time": t.time,
                        "Task": t.title,
                        "Duration (min)": t.duration_minutes,
                        "Priority": t.priority,
                        "Frequency": t.frequency,
                    }
                    for t in pet.get_tasks()
                ]
            )
        else:
            st.caption("No tasks yet.")

st.divider()

st.subheader("Build Schedule")
if st.button("Generate schedule"):
    scheduler = Scheduler(owner)
    plan = scheduler.generate_plan()
    if plan:
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
        st.warning("Nothing to schedule. Add some tasks first.")
    st.text(scheduler.explain_plan())

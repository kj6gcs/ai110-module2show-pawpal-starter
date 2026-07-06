import streamlit as st
from datetime import date

from pawpal_system import Owner, Pet, Task, Scheduler


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

if "owner" not in st.session_state:
    st.session_state.owner = Owner("", "")

if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler()

st.subheader("Owner Profile")

owner_name = st.text_input(
    "Owner Name",
    value=st.session_state.owner.name
)

owner_email = st.text_input(
    "Owner Email",
    value=st.session_state.owner.email
)

if st.button("Save Profile"):
    st.session_state.owner.name = owner_name
    st.session_state.owner.email = owner_email
    st.success("Owner profile updated!")

st.subheader("Add a Pet")

with st.form("add_pet_form"):
    pet_name = st.text_input("Pet name")
    species = st.selectbox("Species", ["dog", "cat", "bird", "reptile", "other"])
    age = st.number_input("Age", min_value=0, max_value=50, value=1)

    submitted_pet = st.form_submit_button("Add Pet")

    if submitted_pet:
        new_pet = Pet(pet_name, species, int(age))
        st.session_state.owner.add_pet(new_pet)
        st.success(f"Added {pet_name}!")

st.markdown("### Current Pets")

pets = st.session_state.owner.get_pets()

if pets:
    pet_rows = [
        {"Name": pet.name, "Species": pet.species, "Age": pet.age}
        for pet in pets
    ]
    st.table(pet_rows)
else:
    st.info("No pets added yet.")

st.divider()

st.subheader("Schedule a Task")

if pets:
    with st.form("add_task_form"):
        selected_pet_name = st.selectbox(
            "Choose pet",
            [pet.name for pet in pets]
        )

        task_title = st.text_input("Task title", value="Morning walk")
        task_type = st.selectbox(
            "Task type",
            ["Feeding", "Exercise", "Medication", "Cleaning", "Grooming", "Enrichment", "Other"]
        )
        due_date = st.date_input("Due date", value=date.today())
        due_time = st.time_input("Due time")
        priority = st.selectbox("Priority", [1, 2, 3], index=1)
        frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])

        submitted_task = st.form_submit_button("Add Task")

        if submitted_task:
            selected_pet = next(
                pet for pet in pets if pet.name == selected_pet_name
            )

            new_task = Task(
                task_title,
                task_type,
                due_date.isoformat(),
                due_time.strftime("%H:%M"),
                int(priority),
                frequency,
)

            st.session_state.scheduler.add_task(new_task, selected_pet)
            st.success(f"Added task for {selected_pet_name}!")
else:
    st.info("Add a pet before scheduling tasks.")

st.divider()

st.subheader("Today's Schedule")

today_tasks = st.session_state.scheduler.get_today_tasks()

if today_tasks:
    sorted_tasks = sorted(today_tasks, key=lambda task: (task.due_time, task.priority))
    st.table([
        {
            "Time": task.due_time,
            "Pet": task.pet_name,
            "Task": task.title,
            "Type": task.task_type,
            "Priority": task.priority,
            "Frequency": task.frequency,
            "Status": "Done" if task.completed else "Pending",
        }
        for task in sorted_tasks
    ])
else:
    st.info("No tasks scheduled for today.")

conflicts = st.session_state.scheduler.detect_conflicts()

if conflicts:
    st.warning("Schedule conflicts found:")
    for conflict in conflicts:
        st.write(f"⚠️ {conflict}")
else:
    st.success("No schedule conflicts detected.")
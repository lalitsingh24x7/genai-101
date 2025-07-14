import streamlit as st
import requests
from datetime import datetime

API_URL = "http://localhost:8080"

st.title("Todo App")

def get_todos():
    resp = requests.get(f"{API_URL}/todos/")
    if resp.status_code == 200:
        return resp.json()
    return []

def create_todo(title: str, description: str, completed: bool):
    data = {"title": title, "description": description, "completed": completed}
    resp = requests.post(f"{API_URL}/todos/", json=data)
    return resp.ok

def update_todo(todo_id: str, title: str, description: str, completed: bool):
    data = {"title": title, "description": description, "completed": completed}
    resp = requests.put(f"{API_URL}/todos/{todo_id}", json=data)
    return resp.ok

def delete_todo(todo_id: str):
    resp = requests.delete(f"{API_URL}/todos/{todo_id}")
    return resp.ok

def is_today(date_str: str) -> bool:
    try:
        return datetime.fromisoformat(date_str).date() == datetime.now().date()
    except Exception:
        return False

def rerun_app():
    if hasattr(st, "rerun"):
        st.rerun()
    else:
        st.experimental_rerun()

# --- UI Section ---

if "show_add_popup" not in st.session_state:
    st.session_state["show_add_popup"] = False

def open_add_popup():
    st.session_state["show_add_popup"] = True

def close_add_popup():
    st.session_state["show_add_popup"] = False

# Top buttons
col_a, col_b = st.columns([1, 5])
with col_a:
    st.button("🔄", on_click=rerun_app)
with col_b:
    st.button("➕ Add Todo", on_click=open_add_popup)

# Fallback popup-like section (without modal)
if st.session_state["show_add_popup"]:
    st.subheader("Add a new Todo")
    with st.form("add_todo_form"):
        title = st.text_input("Title")
        description = st.text_area("Description")
        completed = st.checkbox("Completed", value=False)
        submit, cancel = st.columns(2)
        with submit:
            submitted = st.form_submit_button("Submit")
        with cancel:
            canceled = st.form_submit_button("Cancel")

        if submitted:
            if title:
                if create_todo(title, description, completed):
                    st.success("Todo created!")
                    close_add_popup()
                    rerun_app()
                else:
                    st.error("Failed to create todo.")
            else:
                st.warning("Title is required.")

        if canceled:
            close_add_popup()
            rerun_app()

# Get and show today's todos
todos = get_todos()
today_todos = [todo for todo in todos if is_today(todo["created_at"])]

st.subheader("Today's Todos")
if not today_todos:
    st.info("No todos for today.")

for todo in today_todos:
    with st.expander(f"{todo['title']} (Created: {todo['created_at']})"):
        st.write(f"**Description:** {todo['description']}")
        st.write(f"**Completed:** {'✅' if todo['completed'] else '❌'}")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Delete", key=f"del_{todo['id']}"):
                if delete_todo(todo['id']):
                    st.success("Todo deleted!")
                    rerun_app()
                else:
                    st.error("Failed to delete todo.")
        with col2:
            if st.button("Edit", key=f"edit_{todo['id']}"):
                with st.form(f"edit_form_{todo['id']}"):
                    new_title = st.text_input("Title", value=todo['title'])
                    new_description = st.text_area("Description", value=todo['description'])
                    new_completed = st.checkbox("Completed", value=todo['completed'])
                    update_submitted = st.form_submit_button("Update Todo")
                    if update_submitted:
                        if update_todo(todo['id'], new_title, new_description, new_completed):
                            st.success("Todo updated!")
                            rerun_app()
                        else:
                            st.error("Failed to update todo.")

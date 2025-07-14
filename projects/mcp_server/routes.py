from fastapi import APIRouter, HTTPException, Depends
from typing import List
from uuid import uuid4
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends
from typing import List, Generator, Dict
from uuid import uuid4
from datetime import datetime
from sqlalchemy.orm import Session


from models import Todo, TodoCreate, TodoDB, SessionLocal

router = APIRouter()

def get_db() -> Generator[Session, None, None]:
    """
    Dependency that provides a SQLAlchemy database session.
    Yields:
        db (Session): SQLAlchemy session object.
    Ensures the session is closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/todos/", response_model=Todo)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)) -> Todo:
    """
    Create a new todo item in the database.

    Args:
        todo (TodoCreate): The todo item data from the request body.
        db (Session): Database session (provided by dependency).

    Returns:
        Todo: The created todo item.
    """
    new_todo = TodoDB(
        id=str(uuid4()),
        title=todo.title,
        description=todo.description,
        completed=todo.completed,
        created_at=datetime.utcnow()
    )
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

@router.get("/todos/", response_model=List[Todo])
def get_all_todos(db: Session = Depends(get_db)) -> List[Todo]:
    """
    Retrieve all todo items from the database.

    Args:
        db (Session): Database session (provided by dependency).

    Returns:
        List[Todo]: List of all todo items.
    """
    todos = db.query(TodoDB).all()
    return todos

@router.get("/todos/{todo_id}", response_model=Todo)
def get_todo(todo_id: str, db: Session = Depends(get_db)) -> Todo:
    """
    Retrieve a single todo item by its ID.

    Args:
        todo_id (str): The ID of the todo item.
        db (Session): Database session (provided by dependency).

    Returns:
        Todo: The requested todo item.

    Raises:
        HTTPException: If the todo item is not found.
    """
    todo = db.query(TodoDB).filter(TodoDB.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: str, todo_update: TodoCreate, db: Session = Depends(get_db)) -> Todo:
    """
    Update an existing todo item by its ID.

    Args:
        todo_id (str): The ID of the todo item to update.
        todo_update (TodoCreate): The updated todo data.
        db (Session): Database session (provided by dependency).

    Returns:
        Todo: The updated todo item.

    Raises:
        HTTPException: If the todo item is not found.
    """
    db_todo = db.query(TodoDB).filter(TodoDB.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db_todo.title = todo_update.title
    db_todo.description = todo_update.description
    db_todo.completed = todo_update.completed
    db.commit()
    db.refresh(db_todo)
    return db_todo

@router.delete("/todos/{todo_id}")
def delete_todo(todo_id: str, db: Session = Depends(get_db)) -> Dict[str, str]:
    """
    Delete a todo item by its ID.

    Args:
        todo_id (str): The ID of the todo item to delete.
        db (Session): Database session (provided by dependency).

    Returns:
        dict: A message indicating successful deletion.

    Raises:
        HTTPException: If the todo item is not found.
    """
    db_todo = db.query(TodoDB).filter(TodoDB.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(db_todo)
    db.commit()
    return {"detail": "Todo deleted"}
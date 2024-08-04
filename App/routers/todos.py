from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, models, schemas, database

router = APIRouter()

@router.get("/todos/", response_model=List[schemas.TodoInDB])
def read_todos(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    todos = crud.get_todos(db, skip=skip, limit=limit)
    return todos

@router.post("/todos/", response_model=schemas.TodoInDB)
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(database.get_db)):
    return crud.create_todo(db=db, todo=todo)

@router.put("/todos/{todo_id}", response_model=schemas.TodoInDB)
def update_todo(todo_id: int, todo: schemas.TodoUpdate, db: Session = Depends(database.get_db)):
    db_todo = crud.update_todo(db=db, todo=todo)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo

@router.delete("/todos/{todo_id}", response_model=schemas.TodoInDB)
def delete_todo(todo_id: int, db: Session = Depends(database.get_db)):
    crud.delete_todo(db=db, todo_id=todo_id)
    return {"detail": "Todo deleted"}

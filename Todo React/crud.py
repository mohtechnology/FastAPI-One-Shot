from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from database import get_db
from sqlalchemy.orm import Session
from models import ToDo
from typing import List, Optional

router = APIRouter()

class ToDoCreate(BaseModel):
    title : str
    description : str
    done : bool

class ToDoResponse(ToDoCreate):
    id : int

@router.get('/', response_model=List[ToDoResponse]) 
def Show_Todos(db: Session = Depends(get_db)):
    return db.query(ToDo).all() 

@router.post('/', response_model=ToDoResponse) 
def create_todo(todo: ToDoCreate, db: Session = Depends(get_db)):
    new_todo = ToDo(title=todo.title, description=todo.description, done=todo.done)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo) 
    return new_todo 

@router.get('/{todo_id}', response_model=ToDoResponse)
def update_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(ToDo).filter(ToDo.id == todo_id).first()
    if not db_todo:
        return HTTPException(status_code=404, detail="Todo Not Found")
    return db_todo

@router.put('/{todo_id}', response_model=ToDoResponse)
def update_todo(todo_id: int, todo : ToDoCreate, db: Session = Depends(get_db)):
    db_todo = db.query(ToDo).filter(ToDo.id == todo_id).first()
    if not db_todo:
        return HTTPException(status_code=404, detail="Todo Not Found")
    db_todo.title = todo.title 
    db_todo.description = todo.description
    db_todo.done = todo.done
    db.commit()
    return db_todo

@router.delete('/{todo_id}')
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(ToDo).filter(ToDo.id == todo_id).first()
    if not db_todo:
        return HTTPException(status_code=404, detail="Todo Not Found")
    db.delete(db_todo)
    db.commit()
    return {"message": "Todo Deleted Successfully"}
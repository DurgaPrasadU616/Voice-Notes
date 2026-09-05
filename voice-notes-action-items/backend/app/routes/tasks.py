from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import TaskDB, TaskCreate, TaskUpdate, TaskResponse

router = APIRouter()

@router.get("/tasks", response_model=List[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(TaskDB).order_by(TaskDB.created_at.desc()).all()

@router.post("/tasks", response_model=List[TaskResponse])
def create_tasks_bulk(tasks: List[TaskCreate], db: Session = Depends(get_db)):
    db_tasks = []
    for task_data in tasks:
        db_task = TaskDB(**task_data.model_dump())
        db.add(db_task)
        db_tasks.append(db_task)
    db.commit()
    for db_task in db_tasks:
        db.refresh(db_task)
    return db_tasks

@router.patch("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db)):
    db_task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    update_data = task_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_task, key, value)
        
    db.commit()
    db.refresh(db_task)
    return db_task

@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(db_task)
    db.commit()
    return {"ok": True}

@router.delete("/tasks")
def clear_all_tasks(db: Session = Depends(get_db)):
    db.query(TaskDB).delete()
    db.commit()
    return {"ok": True}

from sqlalchemy.orm import Session
from datetime import datetime as dt
from .models import Goal
from .schemas import GoalCreate

def create_goal_db(db: Session, user_id: int, goal: GoalCreate):
    new_goal = Goal(user_id=user_id,
                    goal_value=goal.value,
                    goal_type=goal.type,
                    goal_category=goal.category)
    db.add(new_goal)
    db.commit()
    db.refresh(new_goal)
    return new_goal

def get_goal_by_id(db: Session, goal_id: int):
    return db.query(Goal).filter(Goal.goal_id == goal_id).first()

def get_goal_by_user(db: Session, user_id: int):
    return db.query(Goal).filter(Goal.user_id == user_id).all()

def update_goal(db: Session, goal_id: int, goal_new_data: GoalCreate):
    goal = get_goal_by_id(db, goal_id)
    if (goal):
        goal.goal_date = dt.fromisoformat(goal_new_data.date)
        goal.goal_value = goal_new_data.value
        goal.goal_category = goal_new_data.category
        goal.goal_description = goal_new_data.description
        db.commit()
        db.refresh(goal)

def delete_goal(db: Session, goal_id: int):   
    goal = get_goal_by_id(db, goal_id)
    if (goal):
        db.delete(goal)
        db.commit()
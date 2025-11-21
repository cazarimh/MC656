from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict

from services import goal_service
from database.config import get_db

from database.schemas import GoalCreate
from dto.goals_dto import (
    GoalRegisterResponse, 
    GoalsListResponse
)

router = APIRouter(
    prefix="/{user_id}/goals",
    tags=["3. Metas (Receitas e Despesas)"] 
)

@router.post(
    "/",
    response_model=GoalRegisterResponse,
    status_code=status.HTTP_201_CREATED
)
def create_goal(
    user_id: int, 
    goal_data: GoalCreate, 
    db: Session = Depends(get_db)
):
    try:
        return goal_service.create_new_goal(
            user_id=user_id, goal_data=goal_data, db=db
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )

@router.get(
    "/",
    response_model=list[GoalsListResponse]
)
def get_goals(
    user_id: int, 
    db: Session = Depends(get_db)
):
    try:
        return goal_service.get_goals_by_user(user_id=user_id, db=db)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )
    
@router.get(
    "/{goal_id}",
    response_model=GoalRegisterResponse
)
def get_goal(
    user_id: int, 
    goal_id: int, 
    db: Session = Depends(get_db)
):
    try:
        return goal_service.get_specific_goal(
            user_id=user_id, goal_id=goal_id, db=db
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- ROTA 4: PUT (Editar) ---
@router.put(
    "/{goal_id}",
    response_model=GoalRegisterResponse
)
def update_goal(
    user_id: int, 
    goal_id: int, 
    goal_data: GoalCreate,
    db: Session = Depends(get_db)
):
    try:
        return goal_service.update_specific_goal(
            user_id=user_id, 
            goal_id=goal_id, 
            goal_data=goal_data, 
            db=db
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- ROTA 5: DELETE (Excluir) ---
@router.delete(
    "/{goal_id}",
    response_model=Dict[str, str]
)
def delete_goal(
    user_id: int, 
    goal_id: int, 
    db: Session = Depends(get_db)
):
    try:
        return goal_service.delete_specific_goal(
            user_id=user_id, goal_id=goal_id, db=db
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    

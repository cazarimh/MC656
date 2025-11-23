from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from database import goals as crud_goals
from database import users as crud_user
from database.schemas import GoalCreate

from dto.goals_dto import GoalRegisterResponse, GoalsListResponse
from mapper.goals_mapper import GoalMapper

from utils.validators import FieldValidator as val

def create_new_goal(
    user_id: int, 
    goal_data: GoalCreate, 
    db: Session
) -> GoalRegisterResponse:
    
    # Valida o usuário
    user = crud_user.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário não cadastrado.",
        )

    goal = crud_goals.get_goal_by_category(db, user_id, goal_data.category)
    if goal:
        return update_specific_goal(user_id, goal.goal_id, goal_data, db)

    # Validações
    val.validate_type(goal_data.type)
    val.validate_category(goal_data.category, goal_data.type)
    val.validate_value(goal_data.value)

    # Chama o crud de meta
    goal_model = crud_goals.create_goal_db(
        db, user.user_id, goal_data
    )
    
    # Converte para o DTO de resposta
    return GoalMapper.to_response(goal_model, db=db)


def get_goals_by_user(
    user_id: int, 
    db: Session
) -> list[GoalsListResponse]:
    
    # Valida o usuário
    user = crud_user.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuário com ID {user_id} não encontrado.",
        )

    # Busca as metas
    goals_list = crud_goals.get_goal_by_user(db, user.user_id)
    
    # Converte para a lista de DTOs de resposta
    return GoalMapper.to_list_response(goals_list, db=db)


def _get_goal_and_verify_user(
    db: Session, user_id: int, goal_id: int
):
    """
    Busca o usuário, busca a meta,
    e verifica se a meta pertence ao usuário.
    Retorna o modelo da meta se tudo estiver OK.
    """
    user = crud_user.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
        
    goal = crud_goals.get_goal_by_id(db, goal_id)
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Goal not found"
        )
        
    if goal.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this goal"
        )
        
    return goal


def get_specific_goal(
    user_id: int, goal_id: int, db: Session
) -> GoalRegisterResponse:
    
    goal_model = _get_goal_and_verify_user(
        db, user_id, goal_id
    )
    
    return GoalMapper.to_response(goal_model, db=db)


def update_specific_goal(
    user_id: int, 
    goal_id: int, 
    goal_data: GoalCreate, 
    db: Session
) -> GoalRegisterResponse:
    
    _get_goal_and_verify_user(db, user_id, goal_id)
    
    # Validações
    val.validate_type(goal_data.type)
    val.validate_category(goal_data.category, goal_data.type)
    val.validate_value(goal_data.value)
        
    crud_goals.update_goal(
        db=db,
        goal_id=goal_id,
        goal_new_data=goal_data
    )
    
    updated_goal_model = crud_goals.get_goal_by_id(
        db, goal_id
    )
    
    return GoalMapper.to_response(updated_goal_model, db=db)


def delete_specific_goal(
    user_id: int, goal_id: int, db: Session
):
    
    _get_goal_and_verify_user(db, user_id, goal_id)
    
    crud_goals.delete_goal(db, goal_id)
    
    return {"detail": "Goal successfully deleted"}

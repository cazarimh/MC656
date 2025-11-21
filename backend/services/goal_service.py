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

    goal = crud_goals.get_goal_by_category(db, goal_data.category)
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
    return GoalMapper.to_response(goal_model)

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
    return GoalMapper.to_list_response(goals_list)

def _get_goal_and_verify_user(
    db: Session, user_id: int, goal_id: int
):
    """
    Busca o usuário, busca a meta,
    e verifica se a meta pertence ao usuário.
    Retorna o modelo da meta se tudo estiver OK.
    """
    # 1. Verifica se o usuário existe
    user = crud_user.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
        
    # 2. Busca a meta
    goal = crud_goals.get_goal_by_id(db, goal_id)
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Goal not found"
        )
        
    # 3. VERIFICAÇÃO DE SEGURANÇA CRUCIAL
    if goal.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this goal"
        )
        
    return goal

# --- FUNÇÃO 2: GET (Específico) ---
def get_specific_goal(
    user_id: int, goal_id: int, db: Session
) -> GoalRegisterResponse:
    
    # Usa a função helper para buscar e verificar a transação
    goal_model = _get_goal_and_verify_user(
        db, user_id, goal_id
    )
    
    # Converte para DTO e retorna
    return GoalMapper.to_response(goal_model)

# --- FUNÇÃO 3: PUT (Editar) ---
def update_specific_goal(
    user_id: int, 
    goal_id: int, 
    goal_data: GoalCreate, 
    db: Session
) -> GoalRegisterResponse:
    
    # Usa a helper para garantir que temos permissão
    _get_goal_and_verify_user(db, user_id, goal_id)
    
    # Validações
    val.validate_type(goal_data.type)

    val.validate_category(goal_data.category, goal_data.type)
    
    val.validate_value(goal_data.value)
        
    # Chama a função de update do banco
    crud_goals.update_goal(
        db=db,
        goal_id=goal_id,
        goal_new_data=goal_data
    )
    
    # Busca o objeto atualizado no banco para retornar
    updated_goal_model = crud_goals.get_goal_by_id(
        db, goal_id
    )
    
    # Converte para DTO e retorna
    return GoalMapper.to_response(updated_goal_model)

# --- FUNÇÃO 4: DELETE (Excluir) ---
def delete_specific_goal(
    user_id: int, goal_id: int, db: Session
):
    
    # Usa a helper
    _get_goal_and_verify_user(db, user_id, goal_id)
    
    # Chama a função de delete do banco
    crud_goals.delete_goal(db, goal_id)
    
    # Retorna uma mensagem de sucesso
    return {"detail": "Goal successfully deleted"}
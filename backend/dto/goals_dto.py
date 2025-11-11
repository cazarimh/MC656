from pydantic import BaseModel


class GoalRegisterResponse(BaseModel):
    goal_id: int
    goal_value: float
    goal_type: str
    goal_category: str


class GoalsListResponse(BaseModel):
    goal_id: int
    goal_value: float
    goal_type: str
    goal_category: str

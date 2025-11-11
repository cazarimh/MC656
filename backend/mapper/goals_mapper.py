from database.models import Goal
from dto.goals_dto import GoalRegisterResponse, GoalsListResponse


class GoalMapper:
    @staticmethod
    def to_response(goal: Goal) -> GoalRegisterResponse:
        return GoalRegisterResponse(
            goal_id=goal.goal_id,
            goal_value=goal.goal_value,
            goal_type=goal.goal_type,
            goal_category=goal.goal_category,
        )

    @staticmethod
    def to_list_response(
        goals: list[Goal],
    ) -> list[GoalsListResponse]:
        return [
            GoalsListResponse(
                goal_id=g.goal_id,
                goal_value=g.goal_value,
                goal_type=g.goal_type,
                goal_category=g.goal_category,
            )
            for g in goals
        ]

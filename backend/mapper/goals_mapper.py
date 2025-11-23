from utils.goals_utils import compute_current_value

class GoalMapper:

    @staticmethod
    def to_response(goal_model, db=None):
        response = {
            "user_id": goal_model.user_id,
            "goal_id": goal_model.goal_id,
            "goal_value": goal_model.goal_value,
            "goal_type": goal_model.goal_type,
            "goal_category": goal_model.goal_category,
        }

        if db:
            response["current_value"] = compute_current_value(
                db=db,
                user_id=goal_model.user_id,
                goal_model=goal_model
            )

        return response

    @staticmethod
    def to_list_response(goals_list, db=None):
        return [
            GoalMapper.to_response(goal, db=db)
            for goal in goals_list
        ]

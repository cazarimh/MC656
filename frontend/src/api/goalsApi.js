import axios from "axios";

const API_URL = "http://localhost:8000";

export async function getGoals(userId) {
  const response = await axios.get(`${API_URL}/${userId}/goals/`);
  return response.data;
}

export async function createGoal(userId, goal) {
  const response = await axios.post(`${API_URL}/${userId}/goals/`, {
    value: goal.value,
    type: goal.type,
    category: goal.goal_category,
  });
  return response.data;
}

export async function updateGoal(userId, goalId, goal) {
  const response = await axios.put(`${API_URL}/${userId}/goals/${goalId}`, {
    value: goal.value,
    type: goal.type,
    category: goal.goal_category,
  });
  return response.data;
}

import axios from "axios";

const API_URL = "http://localhost:8000/users";

export async function registerUser(userData) {
  try {
    const response = await axios.post(`${API_URL}/`, userData);
    return response.data;
  } catch (error) {
    console.error("----- ERRO COMPLETO DO BACKEND -----");
    console.log("response:", error.response);
    console.log("data:", error.response?.data);

    // Se o backend mandou "detail", retornamos ele
    if (error.response && error.response.data && error.response.data.detail) {
      throw new Error(error.response.data.detail);
    }

    // fallback
    throw new Error("Erro ao registrar usuário");
  }
}

export async function loginUser(userData) {
  try {
    const response = await axios.post(`${API_URL}/login`, userData);
    return response.data;
  } catch (error) {
    console.error("Erro no login:", error);

    if (error.response && error.response.data && error.response.data.detail) {
      throw new Error(error.response.data.detail);
    }

    throw new Error("Credenciais inválidas");
  }
}

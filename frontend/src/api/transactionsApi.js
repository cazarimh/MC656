import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",
});

// Criar nova transação
export async function createTransaction(userId, data) {
  try {
    const response = await api.post(`/${userId}/transactions`, data);
    return response.data;
  } catch (err) {
    const backendMsg =
      err.response?.data?.detail || "Erro ao registrar transação.";
    throw new Error(backendMsg);
  }
}

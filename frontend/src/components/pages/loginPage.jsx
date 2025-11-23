import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./loginPage.css";
import { loginUser } from "../../api/userApi";

export default function LoginPage() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ email: "", password: "" });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const result = await loginUser({
        email: form.email,
        password: form.password,
      });

      // salva o user_id vindo do backend
      localStorage.setItem("user_id", result.user_id);

      alert("Login bem-sucedido!");
      navigate("/home");
    } catch (error) {
      console.error("Erro no login:", error);

      const backendMessage =
        error?.response?.data?.detail ||
        error?.response?.data?.error ||
        error?.message ||
        "Credenciais inválidas!";

      alert(backendMessage);
    }
  };

  return (
    <div className="login-container">
      <h1>Finanças Pessoais</h1>
      <form className="login-form" onSubmit={handleSubmit}>
        <h2>Entrar</h2>

        <label>Email</label>
        <input
          type="email"
          name="email"
          value={form.email}
          onChange={handleChange}
          placeholder="seuemail@exemplo.com"
          required
        />

        <label>Senha</label>
        <input
          type="password"
          name="password"
          value={form.password}
          onChange={handleChange}
          placeholder="Digite sua senha"
          required
        />

        <button type="submit" className="login-button">
          Entrar
        </button>

        <p className="register-link">
          Não tem conta?{" "}
          <span onClick={() => navigate("/register")}>Cadastre-se</span>
        </p>
      </form>
    </div>
  );
}

import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./loginPage.css";

export default function LoginPage() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ email: "", password: "" });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    // Por enquanto são dados fictícios apenas para teste
    if (form.email === "teste@teste.com" && form.password === "123456") {
      alert("Login bem-sucedido!");
      navigate("/home"); // vai para a home
    } else {
      alert("Credenciais inválidas!");
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

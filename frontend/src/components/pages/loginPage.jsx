import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import "./loginPage.css";

export default function LoginPage() {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [form, setForm] = useState({ email: "", password: "" });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const payload = {
      email: form.email,
      password: form.password
    };

    try {
      const response = await fetch("http://localhost:8000/users/login",{
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
        });

        if (response.status === 200) {
          const data = await response.json();
          const userData = { id: data.user_id };
          console.log(data);

          login(userData);
          
          navigate("/home");
        } else {
          alert("Credenciais inválidas!");
        }
    } catch (error) {
      alert("Ocorreu um erro inesperado, tente novamente mais tarde");
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

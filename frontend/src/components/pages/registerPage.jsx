import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./registerPage.css";

export default function RegisterPage() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ name: "", email: "", password: "" });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const payload = {
      name: form.name,
      email: form.email,
      password: form.password
    };

    try {
      const response = await fetch("http://localhost:8000/users/",{
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
        });

        if (response.status === 201) {
          alert(`Usuário ${form.name} cadastrado com sucesso!`);
          navigate("/");
        } else {
          let errorData = await response.json();
          alert(errorData.detail)
        }
    } catch (error) {
      alert("Ocorreu um erro inesperado, tente novamente mais tarde");
    }
  };

  return (
    <div className="register-container">
      <h1>Finanças Pessoais</h1>
      <form className="register-form" onSubmit={handleSubmit}>
        <h2>Cadastro</h2>

        <label>Nome</label>
        <input
          type="text"
          name="name"
          value={form.name}
          onChange={handleChange}
          placeholder="Seu nome completo"
          required
        />

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
          placeholder="Crie uma senha"
          required
        />

        <button type="submit" className="register-button">
          Cadastrar
        </button>

        <p className="login-link">
          Já tem conta? <span onClick={() => navigate("/")}>Entrar</span>
        </p>
      </form>
    </div>
  );
}

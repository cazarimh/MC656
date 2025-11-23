import React, { useState } from "react";
import { PlusCircle, ArrowLeft } from "lucide-react";
import { useNavigate } from "react-router-dom";
import "./addIncome.css";
import { createTransaction } from "../../api/transactionsApi";

export default function AddIncome() {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    value: "",
    category: "",
    date: "",
    description: "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const user_id = localStorage.getItem("user_id");
      if (!user_id) {
        alert("Usuário não autenticado!");
        return;
      }

      const payload = {
        type: "income",
        value: Number(formData.value),
        category: formData.category,
        date: formData.date,
        description: formData.description || "",
      };

      await createTransaction(user_id, payload);

      alert("Receita adicionada!");
      navigate("/home");
    } catch (error) {
      alert(error.message);
    }
  };

  return (
    <div style={{ paddingLeft: "1rem" }}>
      <button className="back-button" onClick={() => navigate("/home")}>
        <ArrowLeft size={26} />
        <span>Voltar</span>
      </button>

      <div className="add-income-container">
        <header className="add-income-header">
          <h1>Adicionar Receita</h1>
          <p>Registre suas fontes de renda</p>
        </header>

        <form className="income-form" onSubmit={handleSubmit}>
          <h2 className="income-title">
            <PlusCircle size={20} className="title-icon" />
            Nova Receita
          </h2>

          <div className="form-group">
            <label htmlFor="value">
              Valor <span>*</span>
            </label>
            <input
              id="value"
              name="value"
              type="number"
              placeholder="R$ 0,00"
              value={formData.value}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="category">
              Categoria <span>*</span>
            </label>
            <select
              id="category"
              name="category"
              value={formData.category}
              onChange={handleChange}
              required
            >
              <option value="">Selecione uma categoria</option>
              <option value="salario">Salário</option>
              <option value="freelance">Freelance</option>
              <option value="investimentos">Investimentos</option>
              <option value="outros">Outros</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="date">
              Data <span>*</span>
            </label>
            <input
              id="date"
              name="date"
              type="date"
              value={formData.date}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="description">Descrição (opcional)</label>
            <input
              id="description"
              name="description"
              type="text"
              placeholder="Ex: Pagamento mensal"
              value={formData.description}
              onChange={handleChange}
            />
          </div>

          <button type="submit" className="submit-button">
            <PlusCircle size={18} style={{ marginRight: 8 }} />
            Adicionar Receita
          </button>
        </form>
      </div>
    </div>
  );
}

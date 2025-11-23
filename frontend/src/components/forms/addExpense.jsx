import React, { useState } from "react";
import { MinusCircle, ArrowLeft } from "lucide-react";
import { useNavigate } from "react-router-dom";
import "./addExpense.css";
import { createTransaction } from "../../api/transactionsApi";

export default function AddExpense() {
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
        type: "Despesa",
        value: Number(formData.value),
        category: formData.category,
        date: formData.date,
        description: formData.description || "",
      };

      await createTransaction(user_id, payload);

      alert("Despesa adicionada!");
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

      <div className="add-expense-container">
        <header className="add-expense-header">
          <h1>Adicionar Despesa</h1>
          <p>Registre seus gastos e despesas</p>
        </header>

        <form className="expense-form" onSubmit={handleSubmit}>
          <h2 className="expense-title">
            <MinusCircle size={20} className="title-icon" />
            Nova Despesa
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
              <option value="Moradia">Moradia</option>
              <option value="Alimentação">Alimentação</option>
              <option value="Transporte">Transporte</option>
              <option value="Entretenimento">Entretenimento</option>
              <option value="Utilidades">Utilidades</option>
              <option value="Saúde">Saúde</option>
              <option value="Educação">Educação</option>
              <option value="Outros">Outros</option>
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
              placeholder="Ex: Compras no supermercado"
              value={formData.description}
              onChange={handleChange}
            />
          </div>

          <button type="submit" className="submit-button-expense">
            <MinusCircle size={18} style={{ marginRight: 8 }} />
            Adicionar Despesa
          </button>
        </form>
      </div>
    </div>
  );
}

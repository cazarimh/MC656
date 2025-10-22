// src/components/addExpense.jsx
import React, { useState } from "react";
import { MinusCircle } from "lucide-react";
import "./addExpense.css";

export default function AddExpense() {
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

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Nova Despesa:", formData);
    alert("Despesa adicionada com sucesso!");
  };

  return (
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
            <option value="moradia">Moradia</option>
            <option value="alimentacao">Alimentação</option>
            <option value="transporte">Transporte</option>
            <option value="entretenimento">Entretenimento</option>
            <option value="utilidades">Utilidades</option>
            <option value="saude">Saúde</option>
            <option value="educacao">Educação</option>
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
  );
}

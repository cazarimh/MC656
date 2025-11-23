import React, { useEffect, useState } from "react";
import { ArrowUpDown, Edit, Trash2, Save, X } from "lucide-react";
import "./lancamentos.css";

export default function Lancamentos() {
  const [transactions, setTransactions] = useState([]);
  const [filtered, setFiltered] = useState([]);
  const [sortOrder, setSortOrder] = useState("desc");
  const [filterType, setFilterType] = useState("todos");
  const [filterSubType, setFilterSubType] = useState("");
  const [editing, setEditing] = useState(null);
  const [editData, setEditData] = useState({});

  useEffect(() => {
    async function loadTransactions() {
      try {
        const userId = localStorage.getItem("user_id") || 1;

        const response = await fetch(
          `http://localhost:8000/${userId}/transactions/`
        );
        if (!response.ok) throw new Error("Erro ao buscar transações");

        const data = await response.json();

        console.log("RAW DATA:", data);

        // transforma e garante que nada vire undefined
        const mapped = data.map((t) => ({
          id: t.id ?? t.transaction_id,
          tipo: (t.type ?? t.transaction_type)?.toLowerCase(), // receita / despesa
          subtipo: t.category ?? t.transaction_category,
          valor: t.value ?? t.transaction_value,
          data: t.created_at ?? t.transaction_date,
          description: t.description ?? t.transaction_description,
        }));

        const sorted = mapped.sort((a, b) => {
          if (!a.data) return 1;
          if (!b.data) return -1;
          return new Date(b.data) - new Date(a.data);
        });

        setTransactions(sorted);
        setFiltered(sorted);
      } catch (err) {
        console.error(err);
        alert("Erro ao carregar lançamentos");
      }
    }

    loadTransactions();
  }, []);

  useEffect(() => {
    let result = [...transactions];

    if (filterType !== "todos")
      result = result.filter((t) => t.tipo === filterType);
    if (filterSubType)
      result = result.filter((t) => t.subtipo === filterSubType);

    result.sort((a, b) => {
      if (!a.data) return 1;
      if (!b.data) return -1;

      return sortOrder === "asc"
        ? new Date(a.data) - new Date(b.data)
        : new Date(b.data) - new Date(a.data);
    });

    setFiltered(result);
  }, [filterType, filterSubType, sortOrder, transactions]);

  const toggleSort = () =>
    setSortOrder((prev) => (prev === "asc" ? "desc" : "asc"));

  const handleDelete = async (id) => {
    if (!window.confirm("Tem certeza que deseja excluir este lançamento?"))
      return;

    try {
      const userId = localStorage.getItem("user_id") || 1;

      const response = await fetch(
        `http://localhost:8000/${userId}/transactions/${id}`,
        {
          method: "DELETE",
        }
      );

      if (!response.ok) throw new Error("Erro ao excluir");

      setTransactions(transactions.filter((t) => t.id !== id));
    } catch (err) {
      console.error(err);
      alert("Erro ao excluir lançamento");
    }
  };

  const handleEdit = (t) => {
    setEditing(t.id);
    setEditData({ ...t });
  };

  const handleEditChange = (e) => {
    const { name, value } = e.target;

    if (name === "valor") {
      setEditData((prev) => ({
        ...prev,
        valor: value === "" ? "" : Number(value),
      }));
    } else {
      setEditData((prev) => ({ ...prev, [name]: value }));
    }
  };

  const handleSave = async () => {
    try {
      const userId = localStorage.getItem("user_id") || 1;

      const body = {
        date: editData.data,
        value: editData.valor,
        type: editData.tipo.charAt(0).toUpperCase() + editData.tipo.slice(1),
        category: editData.subtipo,
        description: editData.description || "Atualização",
      };

      const response = await fetch(
        `http://localhost:8000/${userId}/transactions/${editing}`,
        {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(body),
        }
      );

      if (!response.ok) throw new Error("Erro ao atualizar lançamento");

      const updated = await response.json();

      const formatted = {
        id: updated.transaction_id,
        tipo: updated.transaction_type,
        subtipo: updated.transaction_category,
        valor: updated.transaction_value,
        data: updated.transaction_date,
      };

      setTransactions(
        transactions.map((t) => (t.id === editing ? formatted : t))
      );

      setEditing(null);
      setEditData({});
    } catch (err) {
      console.error(err);
      alert("Erro ao salvar alterações");
    }
    window.location.reload();
  };

  const handleCancel = () => {
    setEditing(null);
    setEditData({});
  };

  const tiposFixos = {
    receita: ["Salário", "Freelance", "Investimentos", "Outros"],
    despesa: [
      "Moradia",
      "Alimentação",
      "Transporte",
      "Entretenimento",
      "Utilidades",
      "Saúde",
      "Educação",
      "Outros",
    ],
  };

  const incomeTypes = tiposFixos.receita;
  const expenseTypes = tiposFixos.despesa;

  const formatDateDisplay = (dateStr) => {
    if (!dateStr || typeof dateStr !== "string" || !dateStr.includes("-")) {
      return "Data inválida";
    }

    const [year, month, day] = dateStr.split("-");
    return `${day}/${month}/${year}`;
  };

  return (
    <div className="transactions-page">
      <header className="transactions-header">
        <h1>Lançamentos</h1>
        <p>Gerencie e filtre seus lançamentos financeiros</p>
      </header>

      <div className="filters-container">
        <button className="sort-button" onClick={toggleSort}>
          <ArrowUpDown size={18} />
          {sortOrder === "asc" ? "Data Crescente" : "Data Decrescente"}
        </button>

        <select
          className="filter-select"
          value={filterType}
          onChange={(e) => {
            setFilterType(e.target.value);
            setFilterSubType("");
          }}
        >
          <option value="todos">Todos</option>
          <option value="receita">Somente Receitas</option>
          <option value="despesa">Somente Despesas</option>
        </select>

        {filterType === "receita" && (
          <select
            className="filter-select"
            value={filterSubType}
            onChange={(e) => setFilterSubType(e.target.value)}
          >
            <option value="">Tipo de Receita</option>
            {incomeTypes.map((type) => (
              <option key={type}>{type}</option>
            ))}
          </select>
        )}

        {filterType === "despesa" && (
          <select
            className="filter-select"
            value={filterSubType}
            onChange={(e) => setFilterSubType(e.target.value)}
          >
            <option value="">Tipo de Despesa</option>
            {expenseTypes.map((type) => (
              <option key={type}>{type}</option>
            ))}
          </select>
        )}
      </div>

      <div className="transactions-list">
        {filtered.length > 0 ? (
          filtered.map((t) => (
            <div className="transaction-card" key={t.id}>
              {editing === t.id ? (
                <div className="edit-form">
                  <h3>Editar Lançamento</h3>

                  <label>Tipo</label>
                  <select
                    name="tipo"
                    value={editData.tipo}
                    onChange={handleEditChange}
                  >
                    <option value="receita">Receita</option>
                    <option value="despesa">Despesa</option>
                  </select>

                  <label>Subtipo</label>
                  <select
                    name="subtipo"
                    value={editData.subtipo}
                    onChange={handleEditChange}
                  >
                    <option value="">Selecione...</option>
                    {(editData.tipo === "receita"
                      ? tiposFixos.receita
                      : tiposFixos.despesa
                    ).map((opt) => (
                      <option key={opt} value={opt}>
                        {opt}
                      </option>
                    ))}
                  </select>

                  <label>Valor</label>
                  <input
                    name="valor"
                    type="number"
                    value={editData.valor}
                    onChange={handleEditChange}
                  />

                  <label>Data</label>
                  <input
                    name="data"
                    type="date"
                    value={editData.data}
                    onChange={handleEditChange}
                  />

                  <div className="edit-buttons">
                    <button className="save-button" onClick={handleSave}>
                      <Save size={16} />
                      Salvar
                    </button>
                    <button className="cancel-button" onClick={handleCancel}>
                      <X size={16} />
                      Cancelar
                    </button>
                  </div>
                </div>
              ) : (
                <>
                  <div className="transaction-info">
                    <h3>
                      {t.tipo === "receita" ? "Receita" : "Despesa"} —{" "}
                      {t.subtipo}
                    </h3>
                    <p className="transaction-date">
                      {formatDateDisplay(t.data)}
                    </p>
                  </div>

                  <div className="transaction-actions">
                    <span
                      className={`transaction-value ${
                        t.tipo === "receita" ? "income" : "expense"
                      }`}
                    >
                      R$ {Number(t.valor).toFixed(2)}
                    </span>

                    <button
                      className="edit-button"
                      onClick={() => handleEdit(t)}
                    >
                      <Edit size={16} />
                      Editar
                    </button>
                    <button
                      className="delete-button"
                      onClick={() => handleDelete(t.id)}
                    >
                      <Trash2 size={16} />
                      Excluir
                    </button>
                  </div>
                </>
              )}
            </div>
          ))
        ) : (
          <p className="empty-message">Nenhum lançamento encontrado.</p>
        )}
      </div>
    </div>
  );
}

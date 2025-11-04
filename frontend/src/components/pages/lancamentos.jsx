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
    const fakeData = [
      {
        id: 1,
        tipo: "receita",
        subtipo: "Salário",
        valor: 5000,
        data: "2025-10-30",
      },
      {
        id: 2,
        tipo: "despesa",
        subtipo: "Alimentação",
        valor: 200,
        data: "2025-10-31",
      },
      {
        id: 3,
        tipo: "despesa",
        subtipo: "Transporte",
        valor: 150,
        data: "2025-11-01",
      },
      {
        id: 4,
        tipo: "receita",
        subtipo: "Freelance",
        valor: 800,
        data: "2025-11-01",
      },
      {
        id: 5,
        tipo: "despesa",
        subtipo: "Lazer",
        valor: 200,
        data: "2025-07-09",
      },
    ];

    const sorted = fakeData.sort((a, b) => new Date(b.data) - new Date(a.data));
    setTransactions(sorted);
    setFiltered(sorted);
  }, []);

  useEffect(() => {
    let result = [...transactions];

    if (filterType !== "todos")
      result = result.filter((t) => t.tipo === filterType);
    if (filterSubType)
      result = result.filter((t) => t.subtipo === filterSubType);

    result.sort((a, b) =>
      sortOrder === "asc"
        ? new Date(a.data) - new Date(b.data)
        : new Date(b.data) - new Date(a.data)
    );

    setFiltered(result);
  }, [filterType, filterSubType, sortOrder, transactions]);

  const toggleSort = () =>
    setSortOrder((prev) => (prev === "asc" ? "desc" : "asc"));

  const handleDelete = (id) => {
    if (window.confirm("Tem certeza que deseja excluir este lançamento?")) {
      setTransactions(transactions.filter((t) => t.id !== id));
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

  const handleSave = () => {
    const adjustedDate = editData.data;
    setTransactions(
      transactions.map((t) =>
        t.id === editing ? { ...editData, data: adjustedDate, id: editing } : t
      )
    );
    setEditing(null);
    setEditData({});
  };

  const handleCancel = () => {
    setEditing(null);
    setEditData({});
  };

  // Tipos fixos
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

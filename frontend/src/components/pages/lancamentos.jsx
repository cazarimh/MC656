import React, { useEffect, useState } from "react";
import { useAuth } from "../../context/AuthContext";
import { ArrowUpDown, Edit, Trash2, Save, X } from "lucide-react";
import "./lancamentos.css";

export default function Lancamentos() {

  const getMonthRange = () => {
    const date = new Date();
    const firstDay = new Date(date.getFullYear(), date.getMonth(), 1);
    const lastDay = new Date(date.getFullYear(), date.getMonth() + 1, 0);
    
    const format = (d) => d.toISOString().split('T')[0];
    return { start: format(firstDay), end: format(lastDay) };
  };

  const [dateRange, setDateRange] = useState(getMonthRange());

  const { user } = useAuth();
  const [transactions, setTransactions] = useState([]);
  const [filtered, setFiltered] = useState([]);
  const [sortOrder, setSortOrder] = useState("desc");
  const [filterType, setFilterType] = useState("todos");
  const [filterCategory, setFilterCategory] = useState("");
  const [editing, setEditing] = useState(null);
  const [editData, setEditData] = useState({});
  const [loading, setLoading] = useState(false);

  const fetchTransactions = async () => {
    if (!user || !user.id) {
      navigate("/");
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(`http://localhost:8000/${user.id}/transactions/?start_date=${dateRange.start}&end_date=${dateRange.end}`);

      if (!response.ok) throw new Error("Erro ao buscar transações");
      
      const data = await response.json();

      const mappedData = data.map(item => ({
        transaction_id: item.transaction_id,
        transaction_type: item.transaction_type,
        transaction_category: item.transaction_category,
        transaction_value: item.transaction_value,
        transaction_date: item.transaction_date,
        transaction_description: item.transaction_description
      }));

      const sortedData = mappedData.sort((a, b) => new Date(b.transaction_date) - new Date(a.transaction_date));

      setTransactions(sortedData);
      setFiltered(sortedData);
    } catch (error) {
      console.error("Erro:", error);
      alert("Erro ao carregar lançamentos.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTransactions();
  }, [dateRange]);

  useEffect(() => {
    let result = [...transactions];

    if (filterType !== "todos")
      result = result.filter((t) => t.transaction_type === filterType);
    if (filterCategory)
      result = result.filter((t) => t.transaction_category === filterCategory);

    result.sort((a, b) =>
      sortOrder === "asc"
        ? new Date(a.transaction_date) - new Date(b.transaction_date)
        : new Date(b.transaction_date) - new Date(a.transaction_date)
    );

    setFiltered(result);
  }, [filterType, filterCategory, sortOrder, transactions]);

  const toggleSort = () =>
    setSortOrder((prev) => (prev === "asc" ? "desc" : "asc"));

  const formatDateDisplay = (dateStr) => {
    if (!dateStr) return "-";
    const [year, month, day] = dateStr.split("-");
    return `${day}/${month}/${year}`;
  };

  const handleDelete = async (id) => {
    if (!user || !user.id) {
      navigate("/");
      return;
    }

    if (window.confirm("Tem certeza que deseja excluir este lançamento?")) {
      try {
        const response = await fetch(`http://localhost:8000/${user.id}/transactions/${id}`, {
            method: "DELETE"
        });
        if (response.ok) {
            setTransactions(transactions.filter((t) => t.transaction_id !== id));
        } else {
            alert("Erro ao excluir");
        }
      } catch (error) {
          console.error(error);
      }
    }
  };

  const handleEdit = (t) => {
    setEditing(t.transaction_id);
    setEditData({ ...t });
  };

  const handleEditChange = (e) => {
    const { name, value } = e.target;
    // name deve corresponder às chaves do objeto (transaction_value, etc)
    if (name === "transaction_value") {
      setEditData((prev) => ({
        ...prev,
        transaction_value: value === "" ? "" : Number(value),
      }));
    } else {
      setEditData((prev) => ({ ...prev, [name]: value }));
    }
  };

  const handleSave = async () => {
    if (!user || !user.id) {
      navigate("/");
      return;
    }

    try {
        const payload = {
            type: editData.transaction_type,
            category: editData.transaction_category,
            value: Number(editData.transaction_value),
            date: editData.transaction_date,
            description: editData.transaction_description || ""
        };

        const response = await fetch(`http://localhost:8000/${user.id}/transactions/${editing}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        if (response.ok) {
            const updatedTransaction = await response.json();
            setTransactions(
              transactions.map((t) =>
                t.transaction_id === editing ? { 
                    transaction_id: updatedTransaction.transaction_id,
                    transaction_type: updatedTransaction.transaction_type,
                    transaction_category: updatedTransaction.transaction_category,
                    transaction_value: updatedTransaction.transaction_value,
                    transaction_date: updatedTransaction.transaction_date,
                    transaction_description: updatedTransaction.transaction_description
                } : t
              )
            );
            setEditing(null);
            setEditData({});
        } else {
            alert("Erro ao salvar");
        }
    } catch (error) {
        console.error(error);
        alert("Erro de conexão");
    }
  };

  const handleCancel = () => {
    setEditing(null);
    setEditData({});
  };

  const fixedTypes = {
    receita: ["Salário",
      "Freelance",
      "Investimentos",
      "Outros"
    ],
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

  const incomeTypes = fixedTypes.receita;
  const expenseTypes = fixedTypes.despesa;

  return (
    <div className="transactions-page">
      <header className="transactions-header">
        <h1>Lançamentos</h1>
        <p>Gerencie e filtre seus lançamentos financeiros</p>
      </header>

      <div className="filters-container">
        
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <input 
                type="date" 
                value={dateRange.start} 
                onChange={(e) => setDateRange({...dateRange, start: e.target.value})}
                className="filter-select"
                style={{ cursor: 'pointer' }}
            />
            <span style={{ color: '#64748b', fontSize: '14px' }}>até</span>
            <input 
                type="date" 
                value={dateRange.end} 
                onChange={(e) => setDateRange({...dateRange, end: e.target.value})}
                className="filter-select"
                style={{ cursor: 'pointer' }}
            />
        </div>

        <button className="sort-button" onClick={toggleSort}>
          <ArrowUpDown size={18} />
          {sortOrder === "asc" ? "Data Crescente" : "Data Decrescente"}
        </button>

        <select
          className="filter-select"
          value={filterType}
          onChange={(e) => {
            setFilterType(e.target.value);
            setFilterCategory("");
          }}
        >
          <option value="todos">Todos</option>
          <option value="Receita">Somente Receitas</option>
          <option value="Despesa">Somente Despesas</option>
        </select>

        {filterType === "Receita" && (
          <select
            className="filter-select"
            value={filterCategory}
            onChange={(e) => setFilterCategory(e.target.value)}
          >
            <option value="">Categoria da Receita</option>
            {fixedTypes.receita.map((type) => (
              <option key={type}>{type}</option>
            ))}
          </select>
        )}

        {filterType === "Despesa" && (
          <select
            className="filter-select"
            value={filterCategory}
            onChange={(e) => setFilterCategory(e.target.value)}
          >
            <option value="">Categoria da Despesa</option>
            {fixedTypes.despesa.map((type) => (
              <option key={type}>{type}</option>
            ))}
          </select>
        )}
      </div>

      <div className="transactions-list">
        {loading ? <p>Carregando...</p> : 
         filtered.length > 0 ? (
          filtered.map((t) => (
            <div className="transaction-card" key={t.transaction_id}>
              {editing === t.transaction_id ? (
                <div className="edit-form">
                  <h3>Editar Lançamento</h3>

                  <label>Tipo</label>
                  <select
                    name="transaction_type"
                    value={editData.transaction_type}
                    onChange={handleEditChange}
                  >
                    <option value="Receita">Receita</option>
                    <option value="Despesa">Despesa</option>
                  </select>

                  <label>Categoria</label>
                  <select
                    name="transaction_category"
                    value={editData.transaction_category}
                    onChange={handleEditChange}
                  >
                    <option value="">Selecione...</option>
                    {(editData.transaction_type === "Receita"
                      ? fixedTypes.receita
                      : fixedTypes.despesa
                    ).map((opt) => (
                      <option key={opt} value={opt}>
                        {opt}
                      </option>
                    ))}
                  </select>

                  <label>Valor</label>
                  <input
                    name="transaction_value"
                    type="number"
                    value={editData.transaction_value}
                    onChange={handleEditChange}
                  />

                  <label>Data</label>
                  <input
                    name="transaction_date"
                    type="date"
                    value={editData.transaction_date}
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
                      {t.transaction_type} — {t.transaction_category}
                    </h3>
                    <p className="transaction-date">
                      {formatDateDisplay(t.transaction_date)}
                    </p>
                    <p className="transaction-description">
                      {t.transaction_description}
                    </p>
                  </div>

                  <div className="transaction-actions">
                    <span
                      className={`transaction-value ${
                        t.transaction_type === "Receita" ? "income" : "expense"
                      }`}
                    >
                      R$ {Number(t.transaction_value).toFixed(2)}
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
                      onClick={() => handleDelete(t.transaction_id)}
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
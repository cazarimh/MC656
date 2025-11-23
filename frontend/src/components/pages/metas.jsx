import React, { useState, useEffect } from "react";
import axios from "axios";
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
} from "recharts";
import "./metas.css";

const API_URL = "http://localhost:8000";
const USER_ID = localStorage.getItem("user_id");

export default function Metas() {
  const [goals, setGoals] = useState([]);
  const [form, setForm] = useState({
    tipo: "receita",
    subtipo: "",
    valorMeta: "",
  });

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
  const loadGoals = async (userId) => {
    try {
      const res = await axios.get(`${API_URL}/${userId}/goals`);
      const backendGoals = res.data;

      const converted = backendGoals.map((g) => ({
        id: g.goal_id,
        tipo: g.goal_type.toLowerCase(),
        subtipo: g.goal_category,
        valorMeta: g.goal_value,
        valorAtual: g.current_value ?? 0,
      }));

      setGoals(converted);
    } catch (err) {
      console.error("Erro ao carregar metas:", err);
    }
  };

  useEffect(() => {
    const uid = Number(localStorage.getItem("user_id"));
    if (uid) loadGoals(uid);
  }, []);

  const handleChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();

    const payload = {
      value: Number(form.valorMeta),
      type: form.tipo === "receita" ? "Receita" : "Despesa",
      category: form.subtipo,
    };

    try {
      await axios.post(`${API_URL}/${USER_ID}/goals`, payload);

      await loadGoals(Number(localStorage.getItem("user_id")));

      setForm({ tipo: "receita", subtipo: "", valorMeta: "" });
    } catch (err) {
      console.error("Erro ao criar meta:", err);
      alert("Erro ao salvar meta.");
    }
  };

  const totalByType = (tipo) =>
    goals
      .filter((g) => g.tipo === tipo)
      .reduce(
        (acc, g) => ({
          meta: acc.meta + g.valorMeta,
          atual: acc.atual + g.valorAtual,
        }),
        { meta: 0, atual: 0 }
      );

  const COLORS = ["#2563EB", "#16A34A", "#DC2626", "#CA8A04", "#7C3AED"];

  const receitasTotais = totalByType("receita");
  const despesasTotais = totalByType("despesa");
  const tiposReceita = goals.filter((g) => g.tipo === "receita");
  const tiposDespesa = goals.filter((g) => g.tipo === "despesa");

  return (
    <div className="metas-page">
      <header className="metas-header">
        <h1 style={{ color: "#1E293B" }}>Metas Financeiras</h1>
        <p style={{ color: "#334155" }}>
          Defina suas metas e acompanhe o progresso de receitas e despesas
        </p>
      </header>

      <form className="goal-form" onSubmit={handleSubmit}>
        <select name="tipo" value={form.tipo} onChange={handleChange} required>
          <option value="receita">Receita</option>
          <option value="despesa">Despesa</option>
        </select>

        <select
          name="subtipo"
          value={form.subtipo}
          onChange={handleChange}
          required
        >
          <option value="">Selecione o tipo...</option>
          {tiposFixos[form.tipo].map((tipo) => (
            <option key={tipo} value={tipo}>
              {tipo}
            </option>
          ))}
        </select>

        <input
          type="number"
          name="valorMeta"
          placeholder="Meta (R$)"
          value={form.valorMeta}
          onChange={handleChange}
          required
        />
        <button type="submit">Salvar Meta</button>
      </form>

      <div className="charts-section">
        <div className="chart-card">
          <h3 style={{ color: "#1E293B" }}>Receitas (Geral)</h3>
          <ResponsiveContainer width="100%" height={250}>
            <PieChart>
              <Pie
                data={[
                  { name: "Atingido", value: receitasTotais.atual },
                  {
                    name: "Restante",
                    value: Math.max(
                      receitasTotais.meta - receitasTotais.atual,
                      0
                    ),
                  },
                ]}
                dataKey="value"
                cx="50%"
                cy="50%"
                outerRadius={80}
              >
                <Cell fill="#16A34A" />
                <Cell fill="#475569" />
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="chart-card">
          <h3 style={{ color: "#1E293B" }}>Despesas (Geral)</h3>
          <ResponsiveContainer width="100%" height={250}>
            <PieChart>
              <Pie
                data={[
                  { name: "Gasto", value: despesasTotais.atual },
                  {
                    name: "Disponível",
                    value: Math.max(
                      despesasTotais.meta - despesasTotais.atual,
                      0
                    ),
                  },
                ]}
                dataKey="value"
                cx="50%"
                cy="50%"
                outerRadius={80}
              >
                <Cell fill="#DC2626" />
                <Cell fill="#475569" />
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="chart-bar-container">
        <h3 style={{ color: "#1E293B" }}>Comparativo de Metas por Tipo</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={goals}>
            <CartesianGrid strokeDasharray="3 3" stroke="#475569" />
            <XAxis dataKey="subtipo" stroke="#1E293B" />
            <YAxis stroke="#1E293B" />
            <Tooltip />
            <Legend />
            <Bar dataKey="valorMeta" fill="#94A3B8" name="Meta" />
            <Bar dataKey="valorAtual" fill="#2563EB" name="Atual" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="individual-charts">
        <h3 style={{ color: "#1E293B" }}>Receitas por Tipo</h3>
        <div className="charts-grid">
          {tiposReceita.map((r, i) => (
            <div key={r.id} className="mini-chart-card">
              <h4 style={{ color: "#334155" }}>{r.subtipo}</h4>
              <ResponsiveContainer width="100%" height={200}>
                <PieChart>
                  <Pie
                    data={[
                      { name: "Atingido", value: r.valorAtual },
                      {
                        name: "Restante",
                        value: Math.max(r.valorMeta - r.valorAtual, 0),
                      },
                    ]}
                    dataKey="value"
                    outerRadius={70}
                  >
                    <Cell fill={COLORS[i % COLORS.length]} />
                    <Cell fill="#475569" />
                  </Pie>
                  <Tooltip />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            </div>
          ))}
        </div>

        <h3 style={{ color: "#1E293B" }}>Despesas por Tipo</h3>
        <div className="charts-grid">
          {tiposDespesa.map((d, i) => (
            <div key={d.id} className="mini-chart-card">
              <h4 style={{ color: "#334155" }}>{d.subtipo}</h4>
              <ResponsiveContainer width="100%" height={200}>
                <PieChart>
                  <Pie
                    data={[
                      { name: "Gasto", value: d.valorAtual },
                      {
                        name: "Disponível",
                        value: Math.max(d.valorMeta - d.valorAtual, 0),
                      },
                    ]}
                    dataKey="value"
                    outerRadius={70}
                  >
                    <Cell fill={COLORS[i % COLORS.length]} />
                    <Cell fill="#475569" />
                  </Pie>
                  <Tooltip />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

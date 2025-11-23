import React, { useState, useEffect } from "react";
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

import { getGoals, createGoal, updateGoal } from "../../api/goalsApi";

import "./metas.css";

export default function Metas() {
  const userId = 1; // <-- ajuste se você usa auth
  const [goals, setGoals] = useState([]);
  const [loading, setLoading] = useState(true);

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

  async function loadGoals() {
    try {
      setLoading(true);
      const data = await getGoals(userId);

      const mapped = data.map((g) => ({
        id: g.goal_id,
        tipo: g.goal_type,
        subtipo: g.goal_category,
        valorMeta: g.goal_value,
        valorAtual: 0, // depois integro com lançamentos
      }));

      setGoals(mapped);
    } catch (err) {
      console.error("Erro carregando metas:", err);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadGoals();
  }, []);

  const handleChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();

    const existing = goals.find(
      (g) => g.tipo === form.tipo && g.subtipo === form.subtipo
    );

    const payload = {
      value: Number(form.valorMeta),
      type: form.tipo,
      category: form.subtipo,
    };

    try {
      if (existing) {
        await updateGoal(userId, existing.id, payload);
      } else {
        await createGoal(userId, payload);
      }

      await loadGoals(); // reinicializa tudo atualizado

      setForm({ tipo: "receita", subtipo: "", valorMeta: "" });
    } catch (err) {
      console.error("Erro ao salvar meta:", err);
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

  if (loading) return <p>Carregando...</p>;

  return (
    <div className="metas-page">
      <header className="metas-header">
        <h1>Metas Financeiras</h1>
        <p>Defina suas metas e acompanhe o progresso</p>
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
          <option value="">Selecione...</option>
          {tiposFixos[form.tipo].map((opt) => (
            <option key={opt} value={opt}>
              {opt}
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
          <h3>Receitas (Geral)</h3>
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
          <h3>Despesas (Geral)</h3>
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
        <h3>Comparativo de Metas por Tipo</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={goals}>
            <CartesianGrid strokeDasharray="3 3" stroke="#475569" />
            <XAxis dataKey="subtipo" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="valorMeta" fill="#94A3B8" name="Meta" />
            <Bar dataKey="valorAtual" fill="#2563EB" name="Atual" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="individual-charts">
        <h3>Receitas por Tipo</h3>
        <div className="charts-grid">
          {tiposReceita.map((r, i) => (
            <div key={r.id} className="mini-chart-card">
              <h4>{r.subtipo}</h4>
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

        <h3>Despesas por Tipo</h3>
        <div className="charts-grid">
          {tiposDespesa.map((d, i) => (
            <div key={d.id} className="mini-chart-card">
              <h4>{d.subtipo}</h4>
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

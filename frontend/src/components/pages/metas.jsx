import React, { useState, useEffect } from "react";
import { useAuth } from "../../context/AuthContext";
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

export default function Metas() {

  const getMonthRange = () => {
      const date = new Date();
      const firstDay = new Date(date.getFullYear(), date.getMonth(), 1);
      const lastDay = new Date(date.getFullYear(), date.getMonth() + 1, 0);
      
      const format = (d) => d.toISOString().split('T')[0];
      return { start: format(firstDay), end: format(lastDay) };
    };
  
  const [dateRange, setDateRange] = useState(getMonthRange());

  const { user } = useAuth();
  
  const [goals, setGoals] = useState([]);
  const [loading, setLoading] = useState(true);
  
  const [form, setForm] = useState({
    goal_type: "Receita",
    goal_category: "",
    goal_value: "",
  });

  const fixedTypes = {
    Receita: ["Salário", "Freelance", "Investimentos", "Outros"],
    Despesa: [
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

  const fetchGoalsInfo = async () => {

    if (!user || !user.id) {
      navigate("/");
      return;
    }
    
    setLoading(true);
    try {
      
      const response = await fetch(`http://localhost:8000/${user.id}/goals/info?start_date=${dateRange.start}&end_date=${dateRange.end}`);
      
      if (!response.ok) throw new Error("Falha ao buscar metas");
      
      const data = await response.json();
      setGoals(data);
    } catch (error) {
      console.error("Erro:", error);
      alert("Erro ao carregar metas");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchGoalsInfo();
  }, []);

  const handleChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!user || !user.id) {
      navigate("/");
      return;
    }

    const payload = {
      value: Number(form.goal_value),
      type: form.goal_type,
      category: form.goal_category
    };

     const existingGoal = goals.find(
      (g) => g.goal_type === form.goal_type && g.goal_category === form.goal_category
    );

    try {
      if (payload.value === 0) {
        if (existingGoal) {
          if (window.confirm(`Deseja remover a meta de ${form.goal_category}?`)) {
            const response = await fetch(`http://localhost:8000/${user.id}/goals/${existingGoal.goal_id}`, {
              method: "DELETE",
            });

            if (response.ok) {
              alert("Meta removida com sucesso!");
              setForm({ goal_type: "Receita", goal_category: "", goal_value: "" });
              fetchGoalsInfo();
            } else {
              alert("Erro ao remover meta.");
            }
          }
        } else {
          alert("Insira um valor maior que zero para criar uma meta.");
        }
        return;
      }

      const response = await fetch(`http://localhost:8000/${user.id}/goals/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (response.ok) {
        alert("Meta salva com sucesso!");
        setForm({ goal_type: "Receita", goal_category: "", goal_value: "" });
        fetchGoalsInfo();
      } else {
        alert("Erro ao salvar meta");
      }
    } catch (error) {
      console.error(error);
      alert("Erro de conexão");
    }
  };

  const totalByType = (type) =>
    goals
      .filter((g) => g.goal_type === type)
      .reduce(
        (acc, g) => ({
          meta: acc.meta + g.goal_value,
          atual: acc.atual + (g.goal_progress || 0),
        }),
        { meta: 0, atual: 0 }
      );

  const COLORS = ["#2563EB", "#16A34A", "#DC2626", "#CA8A04", "#7C3AED"];

  const receitasTotais = totalByType("Receita");
  const despesasTotais = totalByType("Despesa");
  
  const tiposReceita = goals.filter((g) => g.goal_type === "Receita");
  const tiposDespesa = goals.filter((g) => g.goal_type === "Despesa");

  if (loading) return <p className="p-4">Carregando metas...</p>;

  return (
    <div className="metas-page">
      <header className="metas-header">
        <h1 style={{ color: "#1E293B" }}>Metas Financeiras</h1>
        <p style={{ color: "#334155" }}>
          Defina suas metas e acompanhe o progresso de receitas e despesas
        </p>
      </header>

      <form className="goal-form" onSubmit={handleSubmit}>
        <select 
          name="goal_type" 
          value={form.goal_type} 
          onChange={handleChange} 
          required
        >
          <option value="Receita">Receita</option>
          <option value="Despesa">Despesa</option>
        </select>

        <select
          name="goal_category"
          value={form.goal_category}
          onChange={handleChange}
          required
        >
          <option value="">Selecione a categoria...</option>
          {fixedTypes[form.goal_type].map((tipo) => (
            <option key={tipo} value={tipo}>
              {tipo}
            </option>
          ))}
        </select>

        <input
          type="number"
          name="goal_value"
          placeholder="Meta (R$)"
          value={form.goal_value}
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
                    value: Math.max(receitasTotais.meta - receitasTotais.atual, 0),
                  },
                ]}
                dataKey="value"
                cx="50%"
                cy="50%"
                outerRadius={80}
              >
                <Cell fill="#16A34A" />
                <Cell fill="#E2E8F0" />
              </Pie>
              <Tooltip formatter={(val) => `R$ ${val.toFixed(2)}`} />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
          <div style={{textAlign: 'center', fontSize: '0.9rem', marginTop: '-10px'}}>
             Progresso: {receitasTotais.meta > 0 ? ((receitasTotais.atual / receitasTotais.meta) * 100).toFixed(1) : 0}%
          </div>
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
                    value: Math.max(despesasTotais.meta - despesasTotais.atual, 0),
                  },
                ]}
                dataKey="value"
                cx="50%"
                cy="50%"
                outerRadius={80}
              >
                <Cell fill={despesasTotais.atual > despesasTotais.meta ? "#DC2626" : "#2563EB"} />
                <Cell fill="#E2E8F0" />
              </Pie>
              <Tooltip formatter={(val) => `R$ ${val.toFixed(2)}`} />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
          <div style={{textAlign: 'center', fontSize: '0.9rem', marginTop: '-10px'}}>
             Uso: {despesasTotais.meta > 0 ? ((despesasTotais.atual / despesasTotais.meta) * 100).toFixed(1) : 0}%
          </div>
        </div>
      </div>

      <div className="chart-bar-container">
        <h3 style={{ color: "#1E293B" }}>Comparativo de Metas por Tipo</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={goals} margin={{top: 20, right: 30, left: 20, bottom: 5}}>
            <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
            <XAxis dataKey="goal_category" stroke="#1E293B" />
            <YAxis stroke="#1E293B" />
            <Tooltip formatter={(val) => `R$ ${val.toFixed(2)}`}/>
            <Legend />
            <Bar dataKey="goal_value" fill="#94A3B8" name="Meta" radius={[4, 4, 0, 0]} />
            <Bar dataKey="goal_progress" fill="#2563EB" name="Atual" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="individual-charts">
        <h3 style={{ color: "#1E293B" }}>Receitas por Categoria</h3>
        <div className="charts-grid">
          {tiposReceita.map((r, i) => (
            <div key={r.goal_id || i} className="mini-chart-card">
              <h4 style={{ color: "#334155" }}>{r.goal_category}</h4>
              <ResponsiveContainer width="100%" height={200}>
                <PieChart>
                  <Pie
                    data={[
                      { name: "Atingido", value: r.goal_progress || 0 },
                      {
                        name: "Restante",
                        value: Math.max(r.goal_value - (r.goal_progress || 0), 0),
                      },
                    ]}
                    dataKey="value"
                    outerRadius={60}
                  >
                    <Cell fill={COLORS[i % COLORS.length]} />
                    <Cell fill="#E2E8F0" />
                  </Pie>
                  <Tooltip formatter={(val) => `R$ ${val.toFixed(2)}`}/>
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
              <p style={{textAlign: 'center', fontSize: '12px'}}>
                {r.goal_progress} / {r.goal_value}
              </p>
            </div>
          ))}
          {tiposReceita.length === 0 && <p className="text-gray-500 italic">Nenhuma meta de receita definida.</p>}
        </div>

        <h3 style={{ color: "#1E293B", marginTop: '30px' }}>Despesas por Categoria</h3>
        <div className="charts-grid">
          {tiposDespesa.map((d, i) => (
            <div key={d.goal_id || i} className="mini-chart-card">
              <h4 style={{ color: "#334155" }}>{d.goal_category}</h4>
              <ResponsiveContainer width="100%" height={200}>
                <PieChart>
                  <Pie
                    data={[
                      { name: "Gasto", value: d.goal_progress || 0 },
                      {
                        name: "Disponível",
                        value: Math.max(d.goal_value - (d.goal_progress || 0), 0),
                      },
                    ]}
                    dataKey="value"
                    outerRadius={60}
                  >
                    <Cell fill={ (d.goal_progress > d.goal_value) ? "#DC2626" : COLORS[i % COLORS.length]} />
                    <Cell fill="#E2E8F0" />
                  </Pie>
                  <Tooltip formatter={(val) => `R$ ${val.toFixed(2)}`}/>
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
              <p style={{textAlign: 'center', fontSize: '12px'}}>
                {d.goal_progress} / {d.goal_value}
              </p>
            </div>
          ))}
          {tiposDespesa.length === 0 && <p className="text-gray-500 italic">Nenhuma meta de despesa definida.</p>}
        </div>
      </div>
    </div>
  );
}
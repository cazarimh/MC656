import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { LogOut } from "lucide-react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
  Cell,
} from "recharts";
import FinancialMetricCard from "../common/financialMetricCard";
import PieChartCard from "../charts/pieChartCard";
import axios from "axios";
import "../pages/home.css";

export default function Home() {
  const [currentMonth] = useState(new Date());
  const [totals, setTotals] = useState(null);
  const [incomeCategories, setIncomeCategories] = useState([]);
  const [expenseCategories, setExpenseCategories] = useState([]);

  const navigate = useNavigate();
  const userId = localStorage.getItem("user_id");

  useEffect(() => {
    async function loadData() {
      try {
        const [totalsRes, incomeRes, expenseRes] = await Promise.all([
          axios.get(`http://localhost:8000/${userId}/dashboard/totals`),
          axios.get(`http://localhost:8000/${userId}/reports/income`),
          axios.get(`http://localhost:8000/${userId}/reports/expenses`),
        ]);

        setTotals(totalsRes.data);
        setIncomeCategories(incomeRes.data);
        setExpenseCategories(expenseRes.data);
      } catch (error) {
        console.error("Erro ao carregar dados do dashboard:", error);
      }
    }

    loadData();
  }, [userId]);

  if (!totals) return <p>Carregando...</p>;

  // TOP 3 receitas/despesas
  const topIncome = incomeCategories
    .sort((a, b) => b.value - a.value)
    .slice(0, 3)
    .map((item, i) => ({
      ...item,
      color: ["#15803D", "#16A34A", "#22C55E"][i],
    }));

  const topExpenses = expenseCategories
    .sort((a, b) => b.value - a.value)
    .slice(0, 3)
    .map((item, i) => ({
      ...item,
      color: ["#991B1B", "#B91C1C", "#DC2626"][i],
    }));

  // Gráfico de barras
  const metasFormatadas = [
    {
      categoria: "Receitas (Geral)",
      progresso: 100, // Apenas exibição
      tipo: "receita",
      valor: totals.total_receitas,
    },
    {
      categoria: "Despesas (Geral)",
      progresso: 100,
      tipo: "despesa",
      valor: totals.total_despesas,
    },
  ];

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <div className="header-left">
          <h1>Página Principal</h1>
          <p className="subtitle">Acompanhe suas receitas e despesas</p>
          <p className="month">
            Mês:{" "}
            {currentMonth.toLocaleString("pt-BR", {
              month: "long",
              year: "numeric",
            })}
          </p>
        </div>

        <button className="logout-button" onClick={() => navigate("/")}>
          <LogOut size={18} />
          <span>Sair</span>
        </button>
      </header>

      <section className="metrics-grid">
        <FinancialMetricCard
          title="Saldo Atual"
          amount={totals.saldo}
          variant="default"
        />
        <FinancialMetricCard
          title="Total Receitas"
          amount={totals.total_receitas}
          variant="income"
          onAddClick={() => navigate("/home/add-income")}
        />
        <FinancialMetricCard
          title="Total Despesas"
          amount={totals.total_despesas}
          variant="expense"
          onAddClick={() => navigate("/home/add-expense")}
        />
      </section>

      <section className="charts-grid">
        <PieChartCard
          title="Top 3 Receitas"
          data={topIncome}
          total={totals.total_receitas}
        />
        <PieChartCard
          title="Top 3 Despesas"
          data={topExpenses}
          total={totals.total_despesas}
        />
      </section>

      <section
        style={{
          marginTop: "40px",
          backgroundColor: "#fff",
          borderRadius: "16px",
          padding: "20px",
          boxShadow: "0 4px 10px rgba(0,0,0,0.1)",
        }}
      >
        <h2 style={{ color: "#1E293B", marginBottom: "20px" }}>
          Comparativo Geral de Receitas x Despesas
        </h2>

        <ResponsiveContainer width="100%" height={250}>
          <BarChart data={metasFormatadas}>
            <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
            <XAxis dataKey="categoria" stroke="#475569" />
            <YAxis stroke="#475569" />
            <Tooltip />
            <Legend />
            <Bar dataKey="valor">
              {metasFormatadas.map((m, i) => (
                <Cell
                  key={i}
                  fill={m.tipo === "receita" ? "#16A34A" : "#DC2626"}
                />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </section>
    </div>
  );
}

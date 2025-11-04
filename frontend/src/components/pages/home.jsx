import React, { useState } from "react";
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
import "../pages/home.css";

export default function Home() {
  const [currentMonth] = useState(new Date());
  const navigate = useNavigate();

  const handleLogout = () => {
    navigate("/");
  };

  const financialData = {
    currentBalance: 12450.75,
    totalIncome: 8500.0,
    totalExpenses: 5234.25,
  };

  const allIncomeData = [
    { name: "Salário", value: 6500 },
    { name: "Freelance", value: 1500 },
    { name: "Investimentos", value: 500 },
    { name: "Outros", value: 300 },
  ];

  const allExpenseData = [
    { name: "Moradia", value: 2000 },
    { name: "Alimentação", value: 800 },
    { name: "Transporte", value: 450 },
    { name: "Lazer", value: 600 },
    { name: "Saúde", value: 300 },
    { name: "Outros", value: 200 },
  ];

  // Top 3 receitas e despesas
  const incomeData = allIncomeData
    .sort((a, b) => b.value - a.value)
    .slice(0, 3)
    .map((item, i) => ({
      ...item,
      color: ["#15803D", "#16A34A", "#22C55E"][i],
    }));

  const expenseData = allExpenseData
    .sort((a, b) => b.value - a.value)
    .slice(0, 3)
    .map((item, i) => ({
      ...item,
      color: ["#991B1B", "#B91C1C", "#DC2626"][i],
    }));

  // Metas gerais
  const metasData = [
    {
      categoria: "Receitas (Geral)",
      atual: 8500,
      meta: 10000,
      tipo: "receita",
    },
    { categoria: "Despesas (Geral)", atual: 5234, meta: 6000, tipo: "despesa" },
  ];

  const metasFormatadas = metasData.map((m) => ({
    categoria: m.categoria,
    progresso: ((m.atual / m.meta) * 100).toFixed(1),
    tipo: m.tipo,
  }));

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

        <button className="logout-button" onClick={handleLogout}>
          <LogOut size={18} />
          <span>Sair</span>
        </button>
      </header>

      <section className="metrics-grid">
        <FinancialMetricCard
          title="Saldo Atual"
          amount={financialData.currentBalance}
          variant="default"
        />
        <FinancialMetricCard
          title="Total Receitas"
          amount={financialData.totalIncome}
          variant="income"
          onAddClick={() => navigate("/home/add-income")}
        />
        <FinancialMetricCard
          title="Total Despesas"
          amount={financialData.totalExpenses}
          variant="expense"
          onAddClick={() => navigate("/home/add-expense")}
        />
      </section>

      <section className="charts-grid">
        <PieChartCard
          title="Top 3 Receitas"
          data={incomeData}
          total={financialData.totalIncome}
        />
        <PieChartCard
          title="Top 3 Despesas"
          data={expenseData}
          total={financialData.totalExpenses}
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
          Progresso das Metas Gerais
        </h2>
        <ResponsiveContainer width="100%" height={250}>
          <BarChart
            data={metasFormatadas}
            layout="vertical"
            margin={{ top: 10, right: 30, left: 50, bottom: 10 }}
          >
            <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
            <XAxis
              type="number"
              domain={[0, 100]}
              tickFormatter={(v) => `${v}%`}
              stroke="#475569"
            />
            <YAxis dataKey="categoria" type="category" stroke="#475569" />
            <Tooltip formatter={(v) => `${v}%`} />
            <Legend />
            <Bar dataKey="progresso" name="Progresso (%)">
              {metasFormatadas.map((entry, index) => (
                <Cell
                  key={`cell-${index}`}
                  fill={entry.tipo === "receita" ? "#16A34A" : "#DC2626"}
                />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </section>
    </div>
  );
}

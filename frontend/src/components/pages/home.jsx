import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { LogOut } from "lucide-react";
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

  const incomeData = [
    { name: "Salário", value: 6500, color: "#388E3C" },
    { name: "Freelance", value: 1500, color: "#66BB6A" },
    { name: "Investimentos", value: 500, color: "#A5D6A7" },
  ];

  const expenseData = [
    { name: "Moradia", value: 2000, color: "#7F0000" },
    { name: "Alimentação", value: 800, color: "#B71C1C" },
    { name: "Transporte", value: 450, color: "#E53935" },
    { name: "Lazer", value: 600, color: "#F28B82" },
  ];

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <div className="header-left">
          <h1>Página Principal</h1>
          <p className="subtitle">Acompanhe suas receitas e despesas</p>

          {/* mês separado em sua própria linha */}
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
          title="Receitas"
          data={incomeData}
          total={financialData.totalIncome}
        />
        <PieChartCard
          title="Despesas"
          data={expenseData}
          total={financialData.totalExpenses}
        />
      </section>
    </div>
  );
}

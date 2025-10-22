import React, { useState } from "react";
import FinancialMetricCard from "./financialMetricCard";
import PieChartCard from "./pieChartCard";

export default function Home() {
  const [currentMonth] = useState(new Date());

  // Dados mock (depois vamos puxar esses dados do backend pela API)
  const financialData = {
    currentBalance: 12450.75,
    totalIncome: 8500.0,
    totalExpenses: 5234.25,
    creditCardBalance: 1850.5,
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
        <div>
          <h1>Página Principal</h1>
          <p>Acompanhe suas receitas e despesas</p>
        </div>
        <div className="month">
          Mês:{" "}
          {currentMonth.toLocaleString("pt-BR", {
            month: "long",
            year: "numeric",
          })}
        </div>
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
        />
        <FinancialMetricCard
          title="Total Despesas"
          amount={financialData.totalExpenses}
          variant="expense"
        />
        <FinancialMetricCard
          title="Cartão"
          amount={financialData.creditCardBalance}
          variant="credit"
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

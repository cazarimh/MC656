import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext"; 
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

  const getMonthRange = () => {
    const date = new Date();
    const firstDay = new Date(date.getFullYear(), date.getMonth(), 1);
    const lastDay = new Date(date.getFullYear(), date.getMonth() + 1, 0);
    
    const format = (d) => d.toISOString().split('T')[0];
    return { start: format(firstDay), end: format(lastDay) };
  };
  
  const [ dateRange, setDateRange ] = useState(getMonthRange());

  const { user, logout } = useAuth();

  const [currentMonth] = useState(new Date());
  const navigate = useNavigate();
  const [ loading, setLoading] = useState(true);
  const [ financialData, setFinancialData ] = useState();
  const [ goalsData, setGoalData ] = useState([]);
  const [ allIncomeData, setAllIncomeData ] = useState([]);
  const [ allExpenseData, setAllExpenseData ] = useState([]);

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  useEffect(() => {
    if (!user || !user.id) {
      navigate("/");
      return;
    }
    
    fetch(`http://localhost:8000/users/${user.id}/info/?start_date=${dateRange.start}&end_date=${dateRange.end}`,{
      method: "GET",
      headers: { "Content-Type": "application/json" },
    })
      .then((response) => {
        if (!response.ok) throw new Error("Error fetching data");
        return response.json();
      })
      .then((data) => {
        setFinancialData(data.financialData);
        setGoalData(data.generalGoals);
        setAllIncomeData(data.incomeList);
        setAllExpenseData(data.expenseList);
      })
      .catch((error) => console.error("Error fetching data: ", error))
      .finally(() => setLoading(false));
  }, []);
  
  if (loading) {
    return <p>loading... </p>
  }

  const totalIncome = financialData.totalIncome;
  const totalExpense = financialData.totalExpense;

  const incomeData = allIncomeData
    .sort((a, b) => b.transaction_value - a.transaction_value)
    .slice(0, 3)
    .map((item, i) => ({
      name: item.transaction_category,
      value: item.transaction_value,
      color: ["#15803D", "#16A34A", "#22C55E"][i],
  }));

  const expenseData = allExpenseData
    .sort((a, b) => b.transaction_value - a.transaction_value)
    .slice(0, 3)
    .map((item, i) => ({
      name: item.transaction_category,
      value: item.transaction_value,
      color: ["#991B1B", "#B91C1C", "#DC2626"][i],
  }));

  const incomeGoals = goalsData.find(g => g.goal_type === "Receita");
  const expenseGoals = goalsData.find(g => g.goal_type === "Despesa");
  const formatedGoals = [
    {
      tipo: "Receita",
      progresso: incomeGoals.goal_value > 0 ?
        Math.min(100, (totalIncome / incomeGoals.goal_value)*100).toFixed(1)
        : 0
    },
    {
      tipo: "Despesa",
      progresso: expenseGoals.goal_value > 0 ?
        Math.min(100, (totalExpense / expenseGoals.goal_value)*100).toFixed(1)
        : 0
    }
  ]

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
          amount={totalIncome}
          variant="income"
          onAddClick={() => navigate("/home/add-income")}
        />
        <FinancialMetricCard
          title="Total Despesas"
          amount={totalExpense}
          variant="expense"
          onAddClick={() => navigate("/home/add-expense")}
        />
      </section>

      <section className="charts-grid">
        <PieChartCard
          title="Top 3 Receitas"
          data={incomeData}
          total={totalIncome}
        />
        <PieChartCard
          title="Top 3 Despesas"
          data={expenseData}
          total={totalExpense}
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
            data={formatedGoals}
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
            <YAxis dataKey="tipo" type="category" stroke="#475569" />
            <Tooltip formatter={(v) => `${v}%`} />
            <Legend />
            <Bar dataKey="progresso" name="Progresso (%)">
              {formatedGoals.map((entry, index) => (
                <Cell
                  key={`cell-${index}`}
                  fill={entry.tipo === "Receita" ? "#16A34A" : "#DC2626"}
                />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </section>
    </div>
  );
}

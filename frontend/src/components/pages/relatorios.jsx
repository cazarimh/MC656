import React, { useEffect, useState } from "react";
import { useAuth } from "../../context/AuthContext";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
} from "recharts";

const COLORS_INCOME = "#16A34A";
const COLORS_EXPENSE = "#DC2626";

const PIE_COLORS = [
  "#16A34A",
  "#DC2626",
  "#64748B",
  "#FACC15",
  "#0EA5E9",
  "#A855F7",
  "#94A3B8",
];

export default function Relatorios() {

  const getMonthRange = () => {
        const date = new Date();
        const firstDay = new Date(date.getFullYear(), date.getMonth(), 1);
        const lastDay = new Date(date.getFullYear(), date.getMonth() + 1, 0);
        
        const format = (d) => d.toISOString().split('T')[0];
        return { start: format(firstDay), end: format(lastDay) };
      };
    
  const [dateRange, setDateRange] = useState(getMonthRange());

  const { user } = useAuth();
  const [loading, setLoading] = useState(true);
  
  const [evolutionData, setEvolutionData] = useState([]);
  const [pieIncomeData, setPieIncomeData] = useState([]);
  const [pieExpenseData, setPieExpenseData] = useState([]);

  useEffect(() => {
    const fetchDashboardInfo = async () => {
      if (!user || !user.id) {
        navigate("/");
        return;
      }
      setLoading(true);
      try {
        const response = await fetch(`http://localhost:8000/${user.id}/transactions/info?start_date=${dateRange.start}&end_date=${dateRange.end}`);
        
        if (!response.ok) throw new Error("Erro ao buscar dados do dashboard");
        
        const data = await response.json();
        
        const evolutionMapped = data.lastYearTransactions.map(item => ({
            mes: item.transaction_month,
            receita: item.month_income,
            despesa: item.month_expense
        }));
        setEvolutionData(evolutionMapped);

        // --- 2. Processar Pizza Receitas ---
        const incomeMapped = data.incomeList.map(item => ({
            name: item.transaction_category,
            value: item.transaction_value
        }));
        setPieIncomeData(incomeMapped);

        // --- 3. Processar Pizza Despesas ---
        const expenseMapped = data.expenseList.map(item => ({
            name: item.transaction_category,
            value: item.transaction_value
        }));
        setPieExpenseData(expenseMapped);

      } catch (error) {
        console.error("Erro:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardInfo();
  }, []);

  if (loading) {
      return (
        <div style={{ padding: "40px", textAlign: "center", minHeight: "100vh", backgroundColor: "#F1F5F9" }}>
            <p style={{color: "#64748B"}}>Gerando relatórios...</p>
        </div>
      );
  }

  return (
    <div
      style={{
        padding: "40px",
        backgroundColor: "#F1F5F9",
        minHeight: "100vh",
        textAlign: "center",
      }}
    >
      <h1
        style={{ fontSize: "2.5rem", color: "#1E293B", marginBottom: "10px" }}
      >
        Relatórios Financeiros
      </h1>
      <p style={{ color: "#334155", marginBottom: "40px" }}>
        Acompanhe a evolução das suas receitas e despesas ao longo do tempo
      </p>

      {/* --- GRÁFICO 1: LINHA (Evolução 12 meses) --- */}
      <div
        style={{
          backgroundColor: "#fff",
          padding: "20px",
          borderRadius: "16px",
          boxShadow: "0 4px 10px rgba(0,0,0,0.1)",
          marginBottom: "40px",
        }}
      >
        <h2 style={{ color: "#1E293B", marginBottom: "20px" }}>
          Evolução de Receitas e Despesas (Últimos 12 Meses)
        </h2>
        <ResponsiveContainer width="100%" height={400}>
          <LineChart data={evolutionData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
            <XAxis dataKey="mes" stroke="#475569" />
            <YAxis stroke="#475569" />
            <Tooltip formatter={(val) => `R$ ${val.toFixed(2)}`} />
            <Legend />
            <Line
              type="monotone"
              dataKey="receita"
              stroke={COLORS_INCOME}
              strokeWidth={3}
              dot={{ r: 5 }}
              activeDot={{ r: 7 }}
              name="Receita"
            />
            <Line
              type="monotone"
              dataKey="despesa"
              stroke={COLORS_EXPENSE}
              strokeWidth={3}
              dot={{ r: 5 }}
              activeDot={{ r: 7 }}
              name="Despesa"
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* --- GRÁFICO 2: BARRAS (Comparativo 12 meses) --- */}
      <div
        style={{
          backgroundColor: "#fff",
          padding: "20px",
          borderRadius: "16px",
          boxShadow: "0 4px 10px rgba(0,0,0,0.1)",
          marginBottom: "40px",
        }}
      >
        <h2 style={{ color: "#1E293B", marginBottom: "20px" }}>
          Comparativo Mensal
        </h2>
        <ResponsiveContainer width="100%" height={400}>
          <BarChart data={evolutionData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
            <XAxis dataKey="mes" stroke="#475569" />
            <YAxis stroke="#475569" />
            <Tooltip formatter={(val) => `R$ ${val.toFixed(2)}`} />
            <Legend />
            <Bar dataKey="receita" fill={COLORS_INCOME} name="Receita" />
            <Bar dataKey="despesa" fill={COLORS_EXPENSE} name="Despesa" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* --- GRÁFICOS DE PIZZA (Por Categoria) --- */}
      <div
        style={{
          display: "flex",
          justifyContent: "center",
          gap: "40px",
          flexWrap: "wrap",
        }}
      >
        {/* Pizza: Despesas */}
        <div
          style={{
            backgroundColor: "#fff",
            padding: "20px",
            borderRadius: "16px",
            boxShadow: "0 4px 10px rgba(0,0,0,0.1)",
            width: "500px",
          }}
        >
          <h2 style={{ color: "#1E293B", marginBottom: "20px" }}>
            Despesas por Categoria
          </h2>
          {pieExpenseData.length > 0 ? (
          <ResponsiveContainer width="100%" height={400}>
            <PieChart>
              <Pie
                data={pieExpenseData}
                dataKey="value"
                nameKey="name"
                cx="50%"
                cy="50%"
                outerRadius={120}
                label
              >
                {pieExpenseData.map((_, i) => (
                  <Cell key={i} fill={PIE_COLORS[i % PIE_COLORS.length]} />
                ))}
              </Pie>
              <Tooltip formatter={(val) => `R$ ${val.toFixed(2)}`} />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
          ) : (
             <p style={{padding: '50px', color: '#94a3b8'}}>Sem despesas registradas.</p>
          )}
        </div>

        {/* Pizza: Receitas */}
        <div
          style={{
            backgroundColor: "#fff",
            padding: "20px",
            borderRadius: "16px",
            boxShadow: "0 4px 10px rgba(0,0,0,0.1)",
            width: "500px",
          }}
        >
          <h2 style={{ color: "#1E293B", marginBottom: "20px" }}>
            Receitas por Categoria
          </h2>
          {pieIncomeData.length > 0 ? (
          <ResponsiveContainer width="100%" height={400}>
            <PieChart>
              <Pie
                data={pieIncomeData}
                dataKey="value"
                nameKey="name"
                cx="50%"
                cy="50%"
                outerRadius={120}
                label
              >
                {pieIncomeData.map((_, i) => (
                  <Cell key={i} fill={PIE_COLORS[i % PIE_COLORS.length]} />
                ))}
              </Pie>
              <Tooltip formatter={(val) => `R$ ${val.toFixed(2)}`} />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
           ) : (
             <p style={{padding: '50px', color: '#94a3b8'}}>Sem receitas registradas.</p>
          )}
        </div>
      </div>
    </div>
  );
}
import { useEffect, useState } from "react";
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
import axios from "axios";

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
  const [dadosMensais, setDadosMensais] = useState([]);
  const [despesasCategorias, setDespesasCategorias] = useState([]);
  const [receitasFixas, setReceitasFixas] = useState([]);

  useEffect(() => {
    async function carregarDados() {
      try {
        const USER_ID = localStorage.getItem("user_id");
        if (!USER_ID) {
          console.error("Usuário não logado!");
          return;
        }

        const monthly = await axios.get(
          `http://localhost:8000/${USER_ID}/reports/monthly`
        );
        const expenses = await axios.get(
          `http://localhost:8000/${USER_ID}/reports/expenses`
        );
        const income = await axios.get(
          `http://localhost:8000/${USER_ID}/reports/income`
        );

        setDadosMensais(monthly.data);
        setDespesasCategorias(expenses.data);
        setReceitasFixas(income.data);
      } catch (err) {
        console.error("Erro ao carregar relatórios:", err);
      }
    }

    carregarDados();
  }, []);

  const comparativo = dadosMensais.map((d) => ({
    mes: d.mes,
    receita: d.receita,
    despesa: d.despesa,
  }));

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

      {/* Gráfico principal de linha */}
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
          Evolução de Receitas e Despesas
        </h2>
        <ResponsiveContainer width="100%" height={400}>
          <LineChart data={dadosMensais}>
            <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
            <XAxis dataKey="mes" stroke="#475569" />
            <YAxis stroke="#475569" />
            <Tooltip />
            <Legend />
            <Line
              type="monotone"
              dataKey="receita"
              stroke="#16A34A"
              strokeWidth={3}
              dot={{ r: 5 }}
              activeDot={{ r: 7 }}
              name="Receita"
            />
            <Line
              type="monotone"
              dataKey="despesa"
              stroke="#DC2626"
              strokeWidth={3}
              dot={{ r: 5 }}
              activeDot={{ r: 7 }}
              name="Despesa"
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Gráfico de barras comparativo */}
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
          Comparativo de Receitas e Despesas Mensais
        </h2>
        <ResponsiveContainer width="100%" height={400}>
          <BarChart data={comparativo}>
            <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
            <XAxis dataKey="mes" stroke="#475569" />
            <YAxis stroke="#475569" />
            <Tooltip />
            <Legend />
            <Bar dataKey="receita" fill="#16A34A" name="Receita" />
            <Bar dataKey="despesa" fill="#DC2626" name="Despesa" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Gráficos de pizza */}
      <div
        style={{
          display: "flex",
          justifyContent: "center",
          gap: "40px",
          flexWrap: "wrap",
        }}
      >
        {/* Despesas */}
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
            Distribuição de Despesas por Categoria
          </h2>
          <ResponsiveContainer width="100%" height={400}>
            <PieChart>
              <Pie
                data={despesasCategorias}
                dataKey="value"
                nameKey="name"
                cx="50%"
                cy="50%"
                outerRadius={120}
                label
              >
                {despesasCategorias.map((_, i) => (
                  <Cell key={i} fill={PIE_COLORS[i % PIE_COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Receitas */}
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
            Distribuição de Receitas Fixas
          </h2>
          <ResponsiveContainer width="100%" height={400}>
            <PieChart>
              <Pie
                data={receitasFixas}
                dataKey="value"
                nameKey="name"
                cx="50%"
                cy="50%"
                outerRadius={120}
                label
              >
                {receitasFixas.map((_, i) => (
                  <Cell key={i} fill={PIE_COLORS[i % PIE_COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}

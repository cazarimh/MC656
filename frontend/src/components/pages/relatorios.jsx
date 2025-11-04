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

const COLORS = ["#16A34A", "#DC2626"];
const PIE_COLORS = [
  "#16A34A",
  "#DC2626",
  "#64748B",
  "#FACC15",
  "#0EA5E9",
  "#A855F7",
  "#94A3B8", // tom mais escuro para “Outros”
];

export default function Relatorios() {
  const dadosMensais = [
    { mes: "Jan", receita: 5300, despesa: 4200 },
    { mes: "Fev", receita: 4800, despesa: 3900 },
    { mes: "Mar", receita: 5500, despesa: 4100 },
    { mes: "Abr", receita: 6000, despesa: 4500 },
    { mes: "Mai", receita: 5800, despesa: 4700 },
    { mes: "Jun", receita: 6100, despesa: 4900 },
    { mes: "Jul", receita: 6400, despesa: 5000 },
    { mes: "Ago", receita: 6300, despesa: 5200 },
    { mes: "Set", receita: 6700, despesa: 5300 },
    { mes: "Out", receita: 7000, despesa: 5500 },
    { mes: "Nov", receita: 6800, despesa: 5400 },
    { mes: "Dez", receita: 7200, despesa: 5600 },
  ];

  const despesasCategorias = [
    { name: "Moradia", value: 1800 },
    { name: "Alimentação", value: 1000 },
    { name: "Transporte", value: 800 },
    { name: "Lazer", value: 600 },
    { name: "Saúde", value: 400 },
    { name: "Outros", value: 300 },
  ];

  const receitasFixas = [
    { name: "Salário", value: 4500 },
    { name: "Freelance", value: 1200 },
    { name: "Investimentos", value: 800 },
    { name: "Outros", value: 500 },
  ];

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

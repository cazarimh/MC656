import React from "react";

function calcPercentages(data, total) {
  return data.map((item) => ({
    ...item,
    percentage: total > 0 ? (item.value / total) * 100 : 0,
  }));
}

export default function PieChartCard({ title, data, total }) {
  const chartData = calcPercentages(data, total);

  let angleAcc = 0;
  const stops = chartData
    .map((item) => {
      const start = angleAcc;
      const end = angleAcc + item.percentage;
      angleAcc = end;
      return `${item.color} ${start}% ${end}%`;
    })
    .join(", ");

  return (
    <div className="pie-card">
      <h3>{title}</h3>
      <div className="pie-body">
        <div className="pie-and-center">
          <div
            className="pie"
            style={{ background: `conic-gradient(${stops})` }}
          />
          <div className="pie-center">
            <div>R$</div>
            <div className="pie-total">
              {Math.round(total).toLocaleString("pt-BR")}
            </div>
          </div>
        </div>

        <div className="pie-legend">
          {chartData.map((item, idx) => (
            <div key={idx} className="legend-row">
              <div
                className="legend-swatch"
                style={{ background: item.color }}
              />
              <div className="legend-label">{item.name}</div>
              <div className="legend-value">
                {Math.round(item.value).toLocaleString("pt-BR")}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

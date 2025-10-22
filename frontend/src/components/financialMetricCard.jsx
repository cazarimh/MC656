import React from "react";

function formatCurrency(value) {
  return new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL",
  }).format(value);
}

export default function FinancialMetricCard({
  title,
  amount,
  variant = "default",
}) {
  const variantClasses = {
    default: "card-default",
    income: "card-income",
    expense: "card-expense",
    credit: "card-credit",
  };
  const cls = variantClasses[variant] || variantClasses.default;

  return (
    <div className={`metric-card ${cls}`}>
      <div className="metric-title">{title}</div>
      <div className="metric-amount">{formatCurrency(amount)}</div>
    </div>
  );
}

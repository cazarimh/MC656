import React from "react";
import { PlusCircle, MinusCircle } from "lucide-react";
import "./financialMetricCard.css";

export default function FinancialMetricCard({
  title,
  amount,
  variant,
  onAddClick,
}) {
  const formattedAmount = amount.toLocaleString("pt-BR", {
    style: "currency",
    currency: "BRL",
  });

  const getVariantClass = () => {
    switch (variant) {
      case "income":
        return "card-income";
      case "expense":
        return "card-expense";
      default:
        return "card-default";
    }
  };

  const Icon =
    variant === "income"
      ? PlusCircle
      : variant === "expense"
      ? MinusCircle
      : null;

  return (
    <div className={`financial-card ${getVariantClass()}`}>
      <div className="card-header">
        <h3>{title}</h3>

        {Icon && (
          <button
            className={`icon-button ${variant}`}
            onClick={onAddClick}
            title={`Adicionar ${variant === "income" ? "receita" : "despesa"}`}
          >
            <Icon size={22} />
          </button>
        )}
      </div>

      <p className="amount">{formattedAmount}</p>
    </div>
  );
}

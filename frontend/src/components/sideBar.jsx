import React from "react";
import { NavLink } from "react-router-dom";
import "./Sidebar.css";
import { LayoutDashboard, TrendingUp, TrendingDown } from "lucide-react";

export default function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <h2>Finanças Pessoais</h2>
        <p>Gerencie seu dinheiro</p>
      </div>

      <nav className="sidebar-nav">
        <NavLink
          to="/home"
          end
          className={({ isActive }) =>
            isActive ? "nav-item active" : "nav-item"
          }
        >
          <LayoutDashboard size={20} className="icon" />
          <span>Dashboard</span>
        </NavLink>

        <NavLink
          to="/home/add-income"
          className={({ isActive }) =>
            isActive ? "nav-item active" : "nav-item"
          }
        >
          <TrendingUp size={20} className="icon" />
          <span>Adicionar Receita</span>
        </NavLink>

        <NavLink
          to="/home/add-expense"
          className={({ isActive }) =>
            isActive ? "nav-item active" : "nav-item"
          }
        >
          <TrendingDown size={20} className="icon" />
          <span>Adicionar Despesa</span>
        </NavLink>
      </nav>
    </aside>
  );
}

// src/components/common/Sidebar.jsx
import React from "react";
import { Link, useLocation } from "react-router-dom";
import { LayoutDashboard, FileText, Target, BarChart3 } from "lucide-react";
import "./Sidebar.css";

export default function Sidebar() {
  const location = useLocation();

  const menuItems = [
    { label: "Dashboard", path: "/home", icon: <LayoutDashboard size={18} /> },
    {
      label: "Lançamentos",
      path: "/home/lancamentos",
      icon: <FileText size={18} />,
    },
    { label: "Metas", path: "/home/metas", icon: <Target size={18} /> },
    {
      label: "Relatórios",
      path: "/home/relatorios",
      icon: <BarChart3 size={18} />,
    },
  ];

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <h2>Finanças Pessoais</h2>
        <p>Gerencie seu dinheiro</p>
      </div>

      <nav className="sidebar-nav">
        {menuItems.map((item) => (
          <Link
            key={item.path}
            to={item.path}
            className={`sidebar-link ${
              location.pathname === item.path ? "active" : ""
            }`}
          >
            {item.icon}
            <span>{item.label}</span>
          </Link>
        ))}
      </nav>
    </aside>
  );
}

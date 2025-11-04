// src/App.jsx
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./components/pages/home";
import AddIncome from "./components/forms/addIncome";
import AddExpense from "./components/forms/addExpense";
import Sidebar from "./components/common/sideBar";
import Login from "./components/pages/loginPage";
import Register from "./components/pages/registerPage";
import Lancamentos from "./components/pages/lancamentos";
import Metas from "./components/pages/metas";
import Relatorios from "./components/pages/relatorios";
import "./App.css";

export default function App() {
  return (
    <Router>
      <Routes>
        {/* Páginas públicas */}
        <Route path="/" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* Layout principal (com Sidebar) */}
        <Route
          path="/home/*"
          element={
            <div className="app-layout">
              <Sidebar />
              <main className="main-content">
                <Routes>
                  <Route index element={<Home />} />
                  <Route path="add-income" element={<AddIncome />} />
                  <Route path="add-expense" element={<AddExpense />} />
                  <Route path="lancamentos" element={<Lancamentos />} />
                  <Route path="metas" element={<Metas />} />
                  <Route path="relatorios" element={<Relatorios />} />
                </Routes>
              </main>
            </div>
          }
        />
      </Routes>
    </Router>
  );
}

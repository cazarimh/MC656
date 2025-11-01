// src/App.jsx
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./components/home";
import AddIncome from "./components/addIncome";
import AddExpense from "./components/addExpense";
import Sidebar from "./components/sideBar";
import Login from "./components/loginPage";
import Register from "./components/registerPage";
import "./App.css";

export default function App() {
  return (
    <Router>
      <Routes>
        {/* Página inicial é o login */}
        <Route path="/" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* Layout principal após login */}
        <Route
          path="/home*"
          element={
            <div className="app-layout">
              <Sidebar />
              <main className="main-content">
                <Routes>
                  <Route index element={<Home />} />
                  <Route path="add-income" element={<AddIncome />} />
                  <Route path="add-expense" element={<AddExpense />} />
                </Routes>
              </main>
            </div>
          }
        />
      </Routes>
    </Router>
  );
}

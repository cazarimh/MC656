import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./components/home";
import AddIncome from "./components/addIncome";
import AddExpense from "./components/addExpense";
import Sidebar from "./components/sideBar";
import "./App.css";

export default function App() {
  return (
    <Router>
      <div className="app-layout">
        <Sidebar />

        <main className="main-content">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/add-income" element={<AddIncome />} />
            <Route path="/add-expense" element={<AddExpense />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

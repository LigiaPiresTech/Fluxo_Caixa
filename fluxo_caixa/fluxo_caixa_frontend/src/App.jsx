import { Routes, Route } from "react-router-dom";
import { AuthProvider } from "./auth/AuthContext";
import ProtectedRoute from "./auth/ProtectedRoute";
import Login from "./auth/Login";
import Layout from "./components/Layout";
import Dashboard from "./pages/Dashboard";
import Usuarios from "./pages/Usuarios";
import Cadastros from "./pages/Cadastros";
import Contas from "./pages/Contas";
import Lancamentos from "./pages/Lancamentos";
import Consolidado from "./pages/Consolidado";
import Relatorios from "./pages/Relatorios";

export default function App() {
  return <AuthProvider>
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route element={<ProtectedRoute><Layout /></ProtectedRoute>}>
        <Route path="/" element={<Dashboard />} />
        <Route path="/usuarios" element={<Usuarios />} />
        <Route path="/cadastros" element={<Cadastros />} />
        <Route path="/contas" element={<Contas />} />
        <Route path="/lancamentos" element={<Lancamentos />} />
        <Route path="/consolidado" element={<Consolidado />} />
        <Route path="/relatorios" element={<Relatorios />} />
      </Route>
    </Routes>
  </AuthProvider>;
}

import { NavLink, Outlet } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";
import {
  LayoutDashboard, Users, Building2, WalletCards, ArrowLeftRight,
  Calculator, FileText, LogOut
} from "lucide-react";

const links = [
  ["/", "Dashboard", LayoutDashboard],
  ["/usuarios", "Usuários", Users],
  ["/cadastros", "Cadastros", Building2],
  ["/contas", "Contas financeiras", WalletCards],
  ["/lancamentos", "Lançamentos", ArrowLeftRight],
  ["/consolidado", "Consolidado", Calculator],
  ["/relatorios", "Relatórios", FileText]
];

export default function Layout() {
  const { user, logout } = useAuth();

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">Fluxo de Caixa</div>
        <nav>
          {links.map(([to, label, Icon]) => (
            <NavLink key={to} to={to} end={to === "/"}>
              <Icon size={18} /> {label}
            </NavLink>
          ))}
        </nav>
        <button className="logout" onClick={logout}><LogOut size={18}/> Sair</button>
      </aside>

      <section className="content">
        <header className="topbar">
          <div>
            <strong>Sistema de Fluxo de Caixa</strong>
            <span className="muted">Ambiente corporativo</span>
          </div>
          <div className="user-badge">{user?.username}</div>
        </header>
        <main className="page"><Outlet /></main>
      </section>
    </div>
  );
}

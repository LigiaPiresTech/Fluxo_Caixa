import { useEffect, useState } from "react";
import { api } from "../api/client";

export default function Dashboard() {
  const [data, setData] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    api.get("/consolidado/saldo", {
      params: {
        id_conta_financeira: 1,
        data_inicio: new Date().toISOString().slice(0, 10),
        data_fim: new Date().toISOString().slice(0, 10)
      }
    }).then(r => setData(r.data)).catch(() => setError("Configure uma conta financeira para visualizar o consolidado."));
  }, []);

  return (
    <>
      <div className="page-title">
        <div><h1>Visão geral</h1><p>Resumo financeiro operacional.</p></div>
      </div>
      {error && <div className="notice">{error}</div>}
      <div className="cards">
        <div className="metric"><span>Créditos</span><strong>R$ {Number(data?.total_creditos || 0).toLocaleString("pt-BR", {minimumFractionDigits: 2})}</strong></div>
        <div className="metric"><span>Débitos</span><strong>R$ {Number(data?.total_debitos || 0).toLocaleString("pt-BR", {minimumFractionDigits: 2})}</strong></div>
        <div className="metric"><span>Saldo</span><strong>R$ {Number(data?.saldo || 0).toLocaleString("pt-BR", {minimumFractionDigits: 2})}</strong></div>
        <div className="metric"><span>Lançamentos</span><strong>{data?.quantidade_lancamentos || 0}</strong></div>
      </div>
      <div className="panel">
        <h2>Arquitetura do front-end</h2>
        <p>React → Cognito → API Gateway → 6 APIs Lambda → RDS Proxy → RDS PostgreSQL.</p>
      </div>
    </>
  );
}

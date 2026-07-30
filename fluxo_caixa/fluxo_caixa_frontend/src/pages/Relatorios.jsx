import { useState } from "react";
import { api } from "../api/client";

export default function Relatorios() {
  const today=new Date().toISOString().slice(0,10);
  const [f,setF]=useState({data_inicio:today,data_fim:today});
  const [rows,setRows]=useState([]);

  async function search(e) {
    e.preventDefault();
    const r=await api.get("/relatorios/fluxo-caixa",{params:f});
    setRows(r.data);
  }

  return <Page title="Relatórios" subtitle="Fluxo de caixa por período.">
    <form className="inline-form" onSubmit={search}>
      <input type="date" value={f.data_inicio} onChange={e=>setF({...f,data_inicio:e.target.value})}/>
      <input type="date" value={f.data_fim} onChange={e=>setF({...f,data_fim:e.target.value})}/>
      <button className="primary">Gerar relatório</button>
    </form>
    <table>
      <thead><tr><th>Data</th><th>Créditos</th><th>Débitos</th><th>Saldo do dia</th></tr></thead>
      <tbody>{rows.map(r=><tr key={String(r.data)}><td>{r.data}</td><td>R$ {Number(r.creditos).toLocaleString("pt-BR",{minimumFractionDigits:2})}</td><td>R$ {Number(r.debitos).toLocaleString("pt-BR",{minimumFractionDigits:2})}</td><td>R$ {Number(r.saldo_dia).toLocaleString("pt-BR",{minimumFractionDigits:2})}</td></tr>)}</tbody>
    </table>
  </Page>;
}
function Page({title,subtitle,children}) { return <><div className="page-title"><div><h1>{title}</h1><p>{subtitle}</p></div></div><div className="panel">{children}</div></>; }

import { useState } from "react";
import { api } from "../api/client";

export default function Consolidado() {
  const today=new Date().toISOString().slice(0,10);
  const [f,setF]=useState({id_conta_financeira:1,data_inicio:today,data_fim:today});
  const [data,setData]=useState(null);

  async function search(e) {
    e.preventDefault();
    const r=await api.get("/consolidado/saldo",{params:f});
    setData(r.data);
  }

  return <Page title="Consolidado" subtitle="Saldo operacional e movimentações confirmadas.">
    <form className="inline-form" onSubmit={search}>
      <input type="number" value={f.id_conta_financeira} onChange={e=>setF({...f,id_conta_financeira:e.target.value})}/>
      <input type="date" value={f.data_inicio} onChange={e=>setF({...f,data_inicio:e.target.value})}/>
      <input type="date" value={f.data_fim} onChange={e=>setF({...f,data_fim:e.target.value})}/>
      <button className="primary">Consultar</button>
    </form>
    {data && <div className="cards compact">
      <div className="metric"><span>Créditos</span><strong>R$ {Number(data.total_creditos).toLocaleString("pt-BR",{minimumFractionDigits:2})}</strong></div>
      <div className="metric"><span>Débitos</span><strong>R$ {Number(data.total_debitos).toLocaleString("pt-BR",{minimumFractionDigits:2})}</strong></div>
      <div className="metric"><span>Saldo</span><strong>R$ {Number(data.saldo).toLocaleString("pt-BR",{minimumFractionDigits:2})}</strong></div>
    </div>}
  </Page>;
}
function Page({title,subtitle,children}) { return <><div className="page-title"><div><h1>{title}</h1><p>{subtitle}</p></div></div><div className="panel">{children}</div></>; }

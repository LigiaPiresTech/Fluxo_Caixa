import { useState } from "react";
import { api } from "../api/client";

const today = new Date().toISOString().slice(0,10);

export default function Lancamentos() {
  const [form,setForm]=useState({
    id_conta_financeira:1,id_conta_contabil:1,tipo_lancamento:"CREDITO",
    descricao:"",valor:"",data_lancamento:today,status:"CONFIRMADO"
  });
  const [msg,setMsg]=useState("");

  async function submit(e) {
    e.preventDefault();
    try {
      const r=await api.post("/lancamentos/lancamentos",{
        ...form,
        id_conta_financeira:Number(form.id_conta_financeira),
        id_conta_contabil:Number(form.id_conta_contabil),
        valor:form.valor
      });
      setMsg(`Lançamento #${r.data.id_lancamento} registrado.`);
    } catch { setMsg("Não foi possível registrar o lançamento."); }
  }

  return <Page title="Lançamentos" subtitle="Registro de débitos e créditos.">
    <form className="form-grid" onSubmit={submit}>
      <label>Tipo<select value={form.tipo_lancamento} onChange={e=>setForm({...form,tipo_lancamento:e.target.value})}><option>CREDITO</option><option>DEBITO</option></select></label>
      <label>Valor<input type="number" step="0.01" min="0.01" value={form.valor} onChange={e=>setForm({...form,valor:e.target.value})} required/></label>
      <label>Conta financeira<input type="number" value={form.id_conta_financeira} onChange={e=>setForm({...form,id_conta_financeira:e.target.value})} required/></label>
      <label>Conta contábil<input type="number" value={form.id_conta_contabil} onChange={e=>setForm({...form,id_conta_contabil:e.target.value})} required/></label>
      <label>Data<input type="date" value={form.data_lancamento} onChange={e=>setForm({...form,data_lancamento:e.target.value})} required/></label>
      <label>Descrição<input value={form.descricao} onChange={e=>setForm({...form,descricao:e.target.value})} required/></label>
      <button className="primary" type="submit">Registrar lançamento</button>
    </form>
    {msg && <div className="notice">{msg}</div>}
  </Page>;
}
function Page({title,subtitle,children}) { return <><div className="page-title"><div><h1>{title}</h1><p>{subtitle}</p></div></div><div className="panel">{children}</div></>; }

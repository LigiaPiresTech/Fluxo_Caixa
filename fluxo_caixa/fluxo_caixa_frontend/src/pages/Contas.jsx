import { useState } from "react";
import { api } from "../api/client";

export default function Contas() {
  const [form, setForm] = useState({id_tipo_conta:1,nome:"",banco:"",saldo_inicial:"0"});
  const [msg,setMsg]=useState("");

  async function submit(e) {
    e.preventDefault();
    try {
      const r=await api.post("/contas/contas-financeiras",{...form,id_tipo_conta:Number(form.id_tipo_conta),saldo_inicial:form.saldo_inicial});
      setMsg(`Conta criada: ${r.data.nome}`);
    } catch { setMsg("Erro ao salvar conta."); }
  }

  return <Page title="Contas financeiras" subtitle="Contas bancárias, caixa e investimentos.">
    <form className="form-grid" onSubmit={submit}>
      <label>Nome<input value={form.nome} onChange={e=>setForm({...form,nome:e.target.value})} required/></label>
      <label>ID tipo de conta<input type="number" value={form.id_tipo_conta} onChange={e=>setForm({...form,id_tipo_conta:e.target.value})} required/></label>
      <label>Banco<input value={form.banco} onChange={e=>setForm({...form,banco:e.target.value})}/></label>
      <label>Saldo inicial<input type="number" step="0.01" value={form.saldo_inicial} onChange={e=>setForm({...form,saldo_inicial:e.target.value})}/></label>
      <button className="primary" type="submit">Salvar conta</button>
    </form>
    {msg && <div className="notice">{msg}</div>}
  </Page>;
}
function Page({title,subtitle,children}) { return <><div className="page-title"><div><h1>{title}</h1><p>{subtitle}</p></div></div><div className="panel">{children}</div></>; }

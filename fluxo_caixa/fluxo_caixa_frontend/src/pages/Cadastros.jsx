import { useState } from "react";
import { api } from "../api/client";

export default function Cadastros() {
  const [tipo, setTipo] = useState("cliente");
  const [form, setForm] = useState({nome_razao_social:"", tipo_pessoa:"JURIDICA", cpf_cnpj:""});
  const [msg, setMsg] = useState("");

  async function submit(e) {
    e.preventDefault();
    try {
      const path = tipo === "cliente" ? "/cadastros/clientes" : "/cadastros/fornecedores";
      const r = await api.post(path, form);
      setMsg(`Cadastro criado: ${r.data.nome_razao_social}`);
    } catch { setMsg("Erro ao salvar cadastro."); }
  }

  return <Page title="Cadastros" subtitle="Clientes e fornecedores.">
    <div className="tabs">
      <button className={tipo==="cliente"?"active":""} onClick={()=>setTipo("cliente")}>Cliente</button>
      <button className={tipo==="fornecedor"?"active":""} onClick={()=>setTipo("fornecedor")}>Fornecedor</button>
    </div>
    <form className="form-grid" onSubmit={submit}>
      <label>Nome / Razão Social<input value={form.nome_razao_social} onChange={e=>setForm({...form,nome_razao_social:e.target.value})} required/></label>
      <label>Tipo de pessoa<select value={form.tipo_pessoa} onChange={e=>setForm({...form,tipo_pessoa:e.target.value})}><option>JURIDICA</option><option>FISICA</option></select></label>
      <label>CPF / CNPJ<input value={form.cpf_cnpj} onChange={e=>setForm({...form,cpf_cnpj:e.target.value})}/></label>
      <button className="primary" type="submit">Salvar</button>
    </form>
    {msg && <div className="notice">{msg}</div>}
  </Page>;
}
function Page({title,subtitle,children}) { return <><div className="page-title"><div><h1>{title}</h1><p>{subtitle}</p></div></div><div className="panel">{children}</div></>; }

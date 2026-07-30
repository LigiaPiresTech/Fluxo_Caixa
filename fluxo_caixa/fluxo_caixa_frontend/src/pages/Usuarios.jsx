import { useState } from "react";
import { api } from "../api/client";

export default function Usuarios() {
  const [form, setForm] = useState({id_perfil: 1, cognito_sub: "", nome: "", email: ""});
  const [message, setMessage] = useState("");

  async function submit(e) {
    e.preventDefault();
    try {
      const r = await api.post("/usuarios/usuarios", {...form, id_perfil: Number(form.id_perfil)});
      setMessage(`Usuário ${r.data.nome} criado.`);
    } catch {
      setMessage("Erro ao criar usuário.");
    }
  }

  return <Page title="Usuários" subtitle="Gestão dos usuários da aplicação e perfis.">
    <form className="form-grid" onSubmit={submit}>
      <Field label="Nome" value={form.nome} onChange={v => setForm({...form,nome:v})}/>
      <Field label="E-mail" value={form.email} onChange={v => setForm({...form,email:v})} type="email"/>
      <Field label="Cognito Sub" value={form.cognito_sub} onChange={v => setForm({...form,cognito_sub:v})}/>
      <Field label="ID do perfil" value={form.id_perfil} onChange={v => setForm({...form,id_perfil:v})} type="number"/>
      <button className="primary" type="submit">Cadastrar usuário</button>
    </form>
    {message && <div className="notice">{message}</div>}
  </Page>;
}

function Field({label,value,onChange,type="text"}) {
  return <label>{label}<input type={type} value={value} onChange={e=>onChange(e.target.value)} required /></label>;
}
function Page({title,subtitle,children}) {
  return <><div className="page-title"><div><h1>{title}</h1><p>{subtitle}</p></div></div><div className="panel">{children}</div></>;
}

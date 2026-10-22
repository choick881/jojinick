"use client";
import { useActionState } from "react";
import { signIn } from "@/app/admin/actions";

export function LoginForm() {
  const [state, action, pending] = useActionState(signIn, undefined);
  return (
    <form action={action} className="card mx-auto grid w-full max-w-sm gap-3.5 p-6">
      <h1 className="title text-[1.5rem]">관리자 로그인</h1>
      <label className="grid gap-1.5"><span className="text-[.85rem] font-bold">이메일</span><input name="email" type="email" autoComplete="username" className="field-input" required /></label>
      <label className="grid gap-1.5"><span className="text-[.85rem] font-bold">비밀번호</span><input name="password" type="password" autoComplete="current-password" className="field-input" required /></label>
      {state?.error && <p role="alert" className="text-[.85rem] font-bold text-accent-deep">{state.error}</p>}
      <button className="btn btn-primary" disabled={pending}>{pending ? "확인 중…" : "로그인"}</button>
    </form>
  );
}

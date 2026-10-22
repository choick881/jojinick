"use client";
import { useActionState, useState } from "react";
import { registerAdmin, signIn } from "@/app/admin/actions";

/** 관리자 로그인. 처음이면 "처음 등록"으로 비밀번호를 정한다(허용된 이메일만, 기한 안에 한 번) */
export function LoginForm() {
  const [mode, setMode] = useState<"login" | "register">("login");
  const [loginState, login, loggingIn] = useActionState(signIn, undefined);
  const [registerState, register, registering] = useActionState(registerAdmin, undefined);
  const isRegister = mode === "register";
  const state = isRegister ? registerState : loginState;
  const pending = isRegister ? registering : loggingIn;

  return (
    <form action={isRegister ? register : login} className="card mx-auto grid w-full max-w-sm gap-3.5 p-6">
      <h1 className="title text-[1.5rem]">{isRegister ? "관리자 처음 등록" : "관리자 로그인"}</h1>
      {isRegister && <p className="text-[.85rem] text-muted">등록이 허락된 이메일로, 앞으로 쓸 비밀번호를 정해 주세요.</p>}
      <label className="grid gap-1.5"><span className="text-[.85rem] font-bold">이메일</span><input name="email" type="email" autoComplete="username" className="field-input" required /></label>
      <label className="grid gap-1.5">
        <span className="text-[.85rem] font-bold">{isRegister ? "새 비밀번호 (8자 이상)" : "비밀번호"}</span>
        <input name="password" type="password" autoComplete={isRegister ? "new-password" : "current-password"} minLength={isRegister ? 8 : undefined} className="field-input" required />
      </label>
      {isRegister && (
        <label className="grid gap-1.5"><span className="text-[.85rem] font-bold">새 비밀번호 한 번 더</span><input name="password2" type="password" autoComplete="new-password" className="field-input" required /></label>
      )}
      {state?.error && <p role="alert" className="text-[.85rem] font-bold text-accent-deep">{state.error}</p>}
      {state?.ok && <p role="status" className="text-[.85rem] font-bold text-brand">{state.ok}</p>}
      <button className="btn btn-primary" disabled={pending}>{pending ? "확인 중…" : isRegister ? "등록하고 로그인" : "로그인"}</button>
      <button type="button" className="text-[.85rem] text-muted underline underline-offset-4" onClick={() => setMode(isRegister ? "login" : "register")}>
        {isRegister ? "이미 등록했어요 → 로그인" : "처음이신가요? 관리자 처음 등록"}
      </button>
    </form>
  );
}

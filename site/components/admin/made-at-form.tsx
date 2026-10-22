"use client";
import { useActionState } from "react";
import { setMadeAt } from "@/app/admin/actions";

export function MadeAtForm({ current }: { current: string }) {
  const [state, action, pending] = useActionState(setMadeAt, undefined);
  return (
    <form action={action} className="flex flex-wrap items-end gap-3">
      <label className="grid gap-1.5"><span className="text-[.85rem] font-bold">오늘 만든 시각</span><input name="madeAt" type="time" defaultValue={current} className="field-input num w-40" required /></label>
      <button className="btn btn-primary" disabled={pending}>{pending ? "저장 중…" : "저장"}</button>
      {state?.error && <p role="alert" className="w-full text-[.85rem] font-bold text-accent-deep">{state.error}</p>}
      {state?.ok && <p role="status" className="w-full text-[.85rem] font-bold text-brand">{state.ok}</p>}
    </form>
  );
}

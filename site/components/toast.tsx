"use client";
import { createContext, useCallback, useContext, useState } from "react";

const ToastContext = createContext<(msg: string) => void>(() => {});

export function ToastProvider({ children }: { children: React.ReactNode }) {
  const [msg, setMsg] = useState<string | null>(null);
  const show = useCallback((m: string) => {
    setMsg(m);
    window.setTimeout(() => setMsg((cur) => (cur === m ? null : cur)), 2000);
  }, []);
  return (
    <ToastContext.Provider value={show}>
      {children}
      <div role="status" aria-live="polite" className="pointer-events-none fixed inset-x-0 z-50 flex justify-center px-4" style={{ bottom: "calc(88px + env(safe-area-inset-bottom, 0px))" }}>
        {msg && <span className="rounded-full bg-ink px-5 py-2.5 text-[.88rem] text-paper shadow-lg">{msg}</span>}
      </div>
    </ToastContext.Provider>
  );
}

export const useToast = () => useContext(ToastContext);

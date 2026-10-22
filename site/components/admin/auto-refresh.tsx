"use client";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

/** 새 주문을 놓치지 않게 화면을 주기적으로 다시 읽는다 */
export function AutoRefresh({ seconds = 60 }: { seconds?: number }) {
  const router = useRouter();
  useEffect(() => {
    const id = setInterval(() => router.refresh(), seconds * 1000);
    return () => clearInterval(id);
  }, [router, seconds]);
  return null;
}

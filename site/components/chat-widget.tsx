"use client";
import Script from "next/script";
import { usePathname } from "next/navigation";
import { CHAT_URL } from "@/lib/site";

/** 손님 화면 오른쪽 아래 AI 상담 말풍선(상담 서버의 embed.js). 관리자 화면에는 띄우지 않는다 */
export function ChatWidget() {
  const pathname = usePathname();
  if (pathname.startsWith("/admin")) return null;
  return <Script src={`${CHAT_URL}/embed.js`} strategy="lazyOnload" />;
}

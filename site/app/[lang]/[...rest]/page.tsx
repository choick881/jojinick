import { notFound } from "next/navigation";

/** 없는 주소는 언어에 맞는 not-found 화면(app/[lang]/not-found.tsx)으로 */
export default function CatchAll() {
  notFound();
}

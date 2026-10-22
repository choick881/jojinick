"use server";
// 관리자 화면의 동작. 매번 로그인·관리자 여부를 다시 확인하고, 쓰기 권한은 DB의 RLS가 한 번 더 막는다.
import { refresh, updateTag } from "next/cache";
import { isClock } from "@/lib/admin";
import { CATALOG_TAG } from "@/lib/catalog";
import { createSessionClient, getAdmin } from "@/lib/supabase/server";

export type FormState = { error?: string; ok?: string } | undefined;

export async function signIn(_: FormState, form: FormData): Promise<FormState> {
  const email = String(form.get("email") ?? "").trim();
  const password = String(form.get("password") ?? "");
  if (!email || !password) return { error: "이메일과 비밀번호를 적어 주세요." };
  const db = await createSessionClient();
  const { error } = await db.auth.signInWithPassword({ email, password });
  if (error) return { error: "이메일 또는 비밀번호가 맞지 않아요." };
  refresh();
  return undefined;
}

export async function signOut() {
  const db = await createSessionClient();
  await db.auth.signOut();
  refresh();
}

export async function setMadeAt(_: FormState, form: FormData): Promise<FormState> {
  const madeAt = String(form.get("madeAt") ?? "");
  if (!isClock(madeAt)) return { error: "시각을 골라 주세요." };
  const { db, isAdmin } = await getAdmin();
  if (!isAdmin) return { error: "관리자만 바꿀 수 있어요." };
  const { error } = await db.from("store_status").update({ made_at: madeAt }).eq("id", 1);
  if (error) return { error: "저장하지 못했어요. 다시 시도해 주세요." };
  updateTag(CATALOG_TAG); // 홈 현황판에 바로 반영
  refresh();
  return { ok: `오늘 제조 시각을 ${madeAt}로 바꿨어요.` };
}

export async function setSoldOut(slug: string, soldOut: boolean) {
  const { db, isAdmin } = await getAdmin();
  if (!isAdmin) return;
  await db.from("products").update({ sold_out: soldOut }).eq("slug", slug);
  updateTag(CATALOG_TAG); // 메뉴·상세 화면에 바로 반영
  refresh();
}

export async function markPickedUp(orderId: string) {
  const { db, isAdmin } = await getAdmin();
  if (!isAdmin) return;
  await db.from("orders").update({ status: "picked_up" }).eq("id", orderId).eq("status", "paid");
  refresh();
}

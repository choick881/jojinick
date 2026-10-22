// 점검용: 서버 키로 주문 DB에 접속되는지 확인한다. 키 값이나 데이터는 돌려주지 않는다.
import { connection, NextResponse } from "next/server";
import { createAdminClient } from "@/lib/supabase/admin";

export async function GET() {
  await connection();
  const db = createAdminClient();
  if (!db) return NextResponse.json({ db: "키 없음 (SUPABASE_SECRET_KEY 미등록)" }, { status: 503 });
  const { error } = await db.from("orders").select("id", { head: true, count: "exact" }).limit(1);
  if (error) return NextResponse.json({ db: "접속 실패", code: error.code ?? null }, { status: 500 });
  return NextResponse.json({ db: "ok" });
}

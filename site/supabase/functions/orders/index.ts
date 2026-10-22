// Supabase Edge Function "orders": 주문 저장·결제 승인·점검·관리자 처음 등록. 비밀 키(SUPABASE_SERVICE_ROLE_KEY)는 Supabase가 함수에 자동으로 넣어 준다.
// 배포: npm run build:edge 로 하나의 파일로 묶은 뒤 Supabase에 올린다(README 참고). 처리 내용은 lib/order-service.ts.
import { createClient } from "npm:@supabase/supabase-js@2";
import { checkHealth, confirmOrder, createOrder, registerAdmin } from "../../../lib/order-service.ts";
import { confirmPayment } from "../../../lib/toss.ts";

const db = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!, {
  auth: { persistSession: false, autoRefreshToken: false },
});
const tossSecret = Deno.env.get("TOSS_SECRET_KEY")?.trim() || undefined; // 없으면 lib/toss.ts의 공개 테스트 키

const json = (body: unknown, status = 200) => new Response(JSON.stringify(body), { status, headers: { "Content-Type": "application/json" } });

Deno.serve(async (req) => {
  if (req.method !== "POST") return json({ error: "METHOD_NOT_ALLOWED" }, 405);
  const { action, payload } = (await req.json().catch(() => ({}))) as { action?: string; payload?: unknown };
  try {
    const result =
      action === "create" ? await createOrder(db, payload, new Date(), crypto.randomUUID())
      : action === "confirm" ? await confirmOrder(db, payload, (input) => confirmPayment(input, fetch, tossSecret))
      : action === "health" ? await checkHealth(db)
      : action === "register-admin" ? await registerAdmin(db, payload, new Date())
      : { status: 400, body: { error: "UNKNOWN_ACTION" } };
    return json(result.body, result.status);
  } catch (e) {
    console.error("[orders] 처리 중 오류:", (e as Error).message);
    return json({ error: "SERVER" }, 500);
  }
});

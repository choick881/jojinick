import "server-only";
// 서버 전용 Supabase 클라이언트. 비밀 키는 RLS를 우회하므로 Route Handler에서만 쓴다.
// 키가 아직 등록되지 않았으면 null을 돌려주고, 호출한 쪽이 '결제 준비 중'으로 안내한다.
import { createClient } from "@supabase/supabase-js";
import { SUPABASE_URL } from "../supabase-config";

export function createAdminClient() {
  // 대시보드에서 붙여넣을 때 섞여 들어가는 앞뒤 공백·줄바꿈을 지운다(남아 있으면 Supabase가 키를 거절)
  const key = process.env.SUPABASE_SECRET_KEY?.trim();
  if (!key) return null;
  return createClient(SUPABASE_URL, key, { auth: { persistSession: false, autoRefreshToken: false } });
}

import "server-only";
// 로그인한 사람의 세션으로 Supabase에 접속한다(publishable 키 + 로그인 쿠키). 권한은 DB의 RLS가 판단한다.
import { createServerClient } from "@supabase/ssr";
import { cookies } from "next/headers";
import { SUPABASE_PUBLISHABLE_KEY, SUPABASE_URL } from "../supabase-config";

export async function createSessionClient() {
  const store = await cookies();
  return createServerClient(SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY, {
    cookies: {
      getAll: () => store.getAll(),
      setAll: (list) => {
        try {
          for (const { name, value, options } of list) store.set(name, value, options);
        } catch {
          // 화면을 그리는 중에는 쿠키를 쓸 수 없다. 로그인 유지는 proxy.ts가 맡는다.
        }
      },
    },
  });
}

/** 지금 로그인한 사람과 관리자 여부. admin_users에는 자기 이메일 줄만 읽을 수 있다(RLS) */
export async function getAdmin() {
  const db = await createSessionClient();
  const {
    data: { user },
  } = await db.auth.getUser();
  if (!user) return { db, email: null, isAdmin: false };
  const { data } = await db.from("admin_users").select("email").maybeSingle();
  return { db, email: user.email ?? null, isAdmin: Boolean(data) };
}

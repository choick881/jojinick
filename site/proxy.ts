// 관리자 화면에서만 로그인 쿠키를 새로 고친다(Supabase 세션 갱신). 다른 경로에는 관여하지 않는다.
import { createServerClient } from "@supabase/ssr";
import { NextResponse, type NextRequest } from "next/server";
import { SUPABASE_PUBLISHABLE_KEY, SUPABASE_URL } from "@/lib/supabase-config";

export async function proxy(request: NextRequest) {
  let response = NextResponse.next({ request });
  const db = createServerClient(SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY, {
    cookies: {
      getAll: () => request.cookies.getAll(),
      setAll: (list) => {
        for (const { name, value } of list) request.cookies.set(name, value);
        response = NextResponse.next({ request });
        for (const { name, value, options } of list) response.cookies.set(name, value, options);
      },
    },
  });
  await db.auth.getUser();
  return response;
}

export const config = { matcher: ["/admin", "/admin/:path*"] };

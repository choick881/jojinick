// 1) 언어 주소: 한국어는 지금 주소 그대로(/menu → 내부적으로 /ko/menu), 영어는 /en/menu. /ko/…로 오면 접두어 없는 주소로 보낸다.
// 2) 관리자 화면에서만 로그인 쿠키를 새로 고친다(Supabase 세션 갱신).
import { createServerClient } from "@supabase/ssr";
import { NextResponse, type NextRequest } from "next/server";
import { routeLocale } from "@/lib/i18n/routing";
import { SUPABASE_PUBLISHABLE_KEY, SUPABASE_URL } from "@/lib/supabase-config";

async function refreshAdminSession(request: NextRequest) {
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

export async function proxy(request: NextRequest) {
  const { pathname } = request.nextUrl;
  if (pathname === "/admin" || pathname.startsWith("/admin/")) return refreshAdminSession(request);

  const route = routeLocale(pathname);
  if (route.action === "pass") return NextResponse.next();
  const url = request.nextUrl.clone();
  url.pathname = route.path;
  return route.action === "redirect" ? NextResponse.redirect(url, 308) : NextResponse.rewrite(url);
}

// _next(빌드 파일)·api·확장자 있는 파일(사진·아이콘·sitemap.xml 등)은 건너뛴다
export const config = { matcher: ["/((?!_next/|api/|.*\\.[a-zA-Z0-9]+$).*)"] };

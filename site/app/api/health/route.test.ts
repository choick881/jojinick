import { beforeEach, describe, expect, it, vi } from "vitest";

// 점검 라우트가 키 값·DB 내용을 내보내지 않고 상태만 알려 주는지 검사한다
let client: unknown = null;
vi.mock("next/server", async (orig) => ({ ...(await orig<typeof import("next/server")>()), connection: async () => {} }));
vi.mock("@/lib/supabase/admin", () => ({ createAdminClient: () => client }));

const { GET } = await import("./route");
const fakeDb = (error: unknown) => ({ from: () => ({ select: () => ({ limit: async () => ({ error }) }) }) });

describe("GET /api/health", () => {
  beforeEach(() => {
    client = null;
  });

  it("키가 없으면 503", async () => {
    expect((await GET()).status).toBe(503);
  });

  it("키가 틀리면 500, 오류 코드만 알려 준다", async () => {
    client = fakeDb({ code: "PGRST301", message: "secret detail" });
    const res = await GET();
    expect(res.status).toBe(500);
    expect(await res.json()).toEqual({ db: "접속 실패", code: "PGRST301" });
  });

  it("접속되면 ok", async () => {
    client = fakeDb(null);
    expect(await (await GET()).json()).toEqual({ db: "ok" });
  });
});

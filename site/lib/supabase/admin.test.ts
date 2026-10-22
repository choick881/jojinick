import { afterEach, describe, expect, it, vi } from "vitest";

vi.mock("server-only", () => ({}));
const createClient = vi.fn(() => ({}));
vi.mock("@supabase/supabase-js", () => ({ createClient }));

const { createAdminClient } = await import("./admin");

describe("createAdminClient", () => {
  afterEach(() => {
    vi.unstubAllEnvs();
    createClient.mockClear();
  });

  it("키가 없거나 공백뿐이면 null", () => {
    vi.stubEnv("SUPABASE_SECRET_KEY", "  \n");
    expect(createAdminClient()).toBeNull();
  });

  it("붙여넣을 때 섞인 앞뒤 공백·줄바꿈을 지운다", () => {
    vi.stubEnv("SUPABASE_SECRET_KEY", " sb_secret_example_abc\n");
    createAdminClient();
    expect(createClient).toHaveBeenCalledWith(expect.any(String), "sb_secret_example_abc", expect.any(Object));
  });
});

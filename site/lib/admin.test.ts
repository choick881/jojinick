import { describe, expect, it } from "vitest";
import { formatPhone, isClock, kstDate } from "./admin";

describe("kstDate", () => {
  it("한국 시각으로 날짜가 바뀐다", () => {
    expect(kstDate(new Date("2026-10-21T14:59:00Z"))).toBe("2026-10-21");
    expect(kstDate(new Date("2026-10-21T15:00:00Z"))).toBe("2026-10-22");
    expect(kstDate(new Date("2026-10-31T16:00:00Z"), 1)).toBe("2026-11-02");
  });
});

describe("formatPhone", () => {
  it("하이픈을 넣는다", () => {
    expect(formatPhone("01012345678")).toBe("010-1234-5678");
    expect(formatPhone("0111234567")).toBe("011-123-4567");
    expect(formatPhone("123")).toBe("123");
  });
});

describe("isClock", () => {
  it("HH:MM만 받는다", () => {
    expect(isClock("07:10")).toBe(true);
    expect(isClock("24:00")).toBe(false);
    expect(isClock("7:10")).toBe(false);
  });
});

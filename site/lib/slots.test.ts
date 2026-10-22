import { describe, expect, it } from "vitest";
import { PICKUP_SLOTS, pickupDays, resolvePickup } from "./slots";

// KST = UTC+9. 테스트 시각은 UTC로 만들어 사용자 PC 시간대와 무관하게 한다.
const kst = (y: number, m: number, d: number, hh: number, mm: number) => new Date(Date.UTC(y, m - 1, d, hh - 9, mm));

describe("pickupDays", () => {
  it("아침에는 오늘의 모든 슬롯과 내일을 연다", () => {
    const days = pickupDays(kst(2026, 10, 21, 9, 0));
    expect(days).toHaveLength(2);
    expect(days[0]).toMatchObject({ date: "2026-10-21", label: "오늘", weekday: "수" });
    expect(days[0].slots.filter((s) => s.open).map((s) => s.time)).toEqual(PICKUP_SLOTS);
    expect(days[1]).toMatchObject({ date: "2026-10-22", label: "내일", weekday: "목" });
  });

  it("슬롯 시작 60분 전에 주문을 마감한다", () => {
    const today = pickupDays(kst(2026, 10, 21, 17, 0))[0];
    expect(today.slots.find((s) => s.time === "17:30")?.open).toBe(false);
    expect(today.slots.find((s) => s.time === "18:00")?.open).toBe(true);
  });

  it("오늘 마지막 슬롯이 마감되면 내일과 모레를 보여 준다", () => {
    const days = pickupDays(kst(2026, 10, 21, 19, 30));
    expect(days.map((d) => d.label)).toEqual(["내일", "모레"]);
    expect(days[0].date).toBe("2026-10-22");
  });

  it("KST 자정을 넘기면 날짜가 바뀐다 (UTC로는 아직 전날)", () => {
    const days = pickupDays(kst(2026, 10, 22, 0, 30));
    expect(days[0]).toMatchObject({ date: "2026-10-22", label: "오늘" });
  });

  it("월말을 넘어가는 날짜를 계산한다", () => {
    const days = pickupDays(kst(2026, 10, 31, 9, 0));
    expect(days[1].date).toBe("2026-11-01");
  });
});

describe("resolvePickup", () => {
  const days = pickupDays(kst(2026, 10, 21, 17, 10));
  it("유효한 선택은 그대로 둔다", () => {
    expect(resolvePickup(days, { date: "2026-10-22", time: "17:30" })).toEqual({ date: "2026-10-22", time: "17:30" });
  });
  it("지난 선택은 가장 이른 가능한 시간으로 바꾼다", () => {
    expect(resolvePickup(days, { date: "2026-10-21", time: "17:30" })).toEqual({ date: "2026-10-21", time: "18:30" });
    expect(resolvePickup(days, null)).toEqual({ date: "2026-10-21", time: "18:30" });
  });
});

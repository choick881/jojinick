// 픽업 날짜·시간 계산. 가게 기준 시간대는 한국(KST, UTC+9, 서머타임 없음).

export const PICKUP_SLOTS = ["17:30", "18:00", "18:30", "19:00", "19:30", "20:00"];
export const SLOT_MINUTES = 30;
/** 슬롯 시작 몇 분 전에 주문을 마감할지 */
export const ORDER_LEAD_MINUTES = 60;

const KST_OFFSET_MS = 9 * 60 * 60 * 1000;
const WEEKDAYS = ["일", "월", "화", "수", "목", "금", "토"];
const LABELS = ["오늘", "내일", "모레"];

export type PickupSlot = { time: string; end: string; open: boolean };
export type PickupDay = { date: string; label: string; weekday: string; month: number; day: number; slots: PickupSlot[] };

const pad = (n: number) => String(n).padStart(2, "0");
const toMinutes = (t: string) => Number(t.slice(0, 2)) * 60 + Number(t.slice(3));
const fromMinutes = (m: number) => `${pad(Math.floor(m / 60))}:${pad(m % 60)}`;

/** 지금 시각 기준으로 주문 가능한 픽업 날짜 2개(오늘이 끝났으면 내일·모레)를 돌려준다. */
export function pickupDays(now: Date): PickupDay[] {
  const kst = new Date(now.getTime() + KST_OFFSET_MS); // UTC getter로 읽으면 KST 값
  const nowMinutes = kst.getUTCHours() * 60 + kst.getUTCMinutes();

  const days: PickupDay[] = [];
  for (let offset = 0; offset < 3 && days.length < 2; offset++) {
    const d = new Date(Date.UTC(kst.getUTCFullYear(), kst.getUTCMonth(), kst.getUTCDate() + offset));
    const slots = PICKUP_SLOTS.map((time) => ({
      time,
      end: fromMinutes(toMinutes(time) + SLOT_MINUTES),
      open: offset > 0 || toMinutes(time) - ORDER_LEAD_MINUTES >= nowMinutes,
    }));
    if (!slots.some((s) => s.open)) continue;
    days.push({
      date: `${d.getUTCFullYear()}-${pad(d.getUTCMonth() + 1)}-${pad(d.getUTCDate())}`,
      label: LABELS[offset],
      weekday: WEEKDAYS[d.getUTCDay()],
      month: d.getUTCMonth() + 1,
      day: d.getUTCDate(),
      slots,
    });
  }
  return days;
}

/** 서버 검증용: 해당 날짜·시간이 지금 주문 가능한지 */
export function isSlotOpen(date: string, time: string, now: Date): boolean {
  return pickupDays(now).some((d) => d.date === date && d.slots.some((s) => s.time === time && s.open));
}

/** 저장된 선택이 아직 유효하면 그대로, 아니면 가장 이른 가능한 시간 */
export function resolvePickup(days: PickupDay[], chosen: { date: string; time: string } | null): { date: string; time: string } | null {
  if (chosen && days.some((d) => d.date === chosen.date && d.slots.some((s) => s.time === chosen.time && s.open))) return chosen;
  const d = days[0];
  const s = d?.slots.find((x) => x.open);
  return d && s ? { date: d.date, time: s.time } : null;
}

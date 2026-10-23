"use client";
import { useMinute } from "@/lib/browser-store";
import { PICKUP_SLOTS, pickupDays, resolvePickup } from "@/lib/slots";
import { useCart } from "./cart";
import { useT } from "./lang";

/** 지금 화면에 보이는 픽업 선택(저장된 값이 지났으면 가장 이른 시간). 결제 때 서버가 다시 검사한다. */
export function useEffectivePickup() {
  const minute = useMinute();
  const { pickup, setPickup } = useCart();
  const days = minute === null ? null : pickupDays(new Date(minute * 60_000));
  return { days, pickup: days ? resolvePickup(days, pickup) : null, setPickup };
}

/** 픽업 날짜·시간 고르기. 시간 계산은 브라우저에서 한다(서버 렌더 시각과 다르므로). */
export function PickupPicker() {
  const { days, pickup, setPickup } = useEffectivePickup();
  const t = useT().pickup;
  // 날짜 이름(오늘·내일·모레)과 요일은 화면 언어로 바꿔 보여 준다
  const dayLabel = (label: string) => t.dayLabels[["오늘", "내일", "모레"].indexOf(label)] ?? label;
  const weekday = (date: string) => t.weekdays[new Date(`${date}T00:00:00Z`).getUTCDay()] ?? "";

  // 서버 렌더·hydration 전: 같은 모양의 자리를 먼저 그려 화면이 밀리지 않게 한다
  const loading = !days;
  const day = days ? (days.find((d) => d.date === pickup?.date) ?? days[0]) : null;
  const dateChips = days ?? [{ date: "a", label: "오늘", month: 0, day: 0, weekday: "", slots: [] }, { date: "b", label: "내일", month: 0, day: 0, weekday: "", slots: [] }];
  const chipText = (d: (typeof dateChips)[number]) => t.chip(dayLabel(d.label), d.month, d.day, d.weekday ? weekday(d.date) : t.weekdays[3]);
  const slotChips = day?.slots ?? PICKUP_SLOTS.map((time) => ({ time, end: "", open: false }));

  return (
    <div className="grid gap-4" aria-busy={loading}>
      <div className="grid gap-2">
        <span className="text-[.85rem] font-bold">{t.date}</span>
        <div className="flex flex-wrap gap-2" role="group" aria-label={t.date}>
          {dateChips.map((d) => (
            <button key={d.date} type="button" className={`chip num ${loading ? "invisible" : ""}`} disabled={loading} aria-pressed={d.date === day?.date}
              onClick={() => setPickup({ date: d.date, time: d.slots.find((s) => s.open)?.time ?? "" })}>
              {chipText(d)}
            </button>
          ))}
        </div>
      </div>
      <div className="grid gap-2">
        <span className="text-[.85rem] font-bold">{t.time} <small className="font-normal text-muted">{t.every30}</small></span>
        <div className="flex flex-wrap gap-2" role="group" aria-label={t.time}>
          {slotChips.map((s) => (
            <button key={s.time} type="button" className={`chip num ${loading ? "opacity-40" : ""}`} disabled={!s.open} aria-pressed={Boolean(day) && pickup?.date === day?.date && pickup?.time === s.time}
              title={loading ? undefined : s.open ? `${s.time}~${s.end}` : t.closed} onClick={() => day && setPickup({ date: day.date, time: s.time })}>
              {s.time}
            </button>
          ))}
        </div>
        <small className="text-[.74rem] text-muted">{t.lead}</small>
      </div>
    </div>
  );
}

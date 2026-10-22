// 관리자 화면에서 쓰는 순수 함수(날짜·전화번호 표시, 주문 상태 이름).

/** 한국 시각 기준 날짜(YYYY-MM-DD). offsetDays=1이면 내일 */
export function kstDate(now: Date, offsetDays = 0): string {
  return new Date(now.getTime() + 9 * 3600_000 + offsetDays * 86_400_000).toISOString().slice(0, 10);
}

/** 01012345678 → 010-1234-5678 */
export function formatPhone(digits: string): string {
  const d = digits.replace(/\D/g, "");
  if (d.length === 11) return `${d.slice(0, 3)}-${d.slice(3, 7)}-${d.slice(7)}`;
  if (d.length === 10) return `${d.slice(0, 3)}-${d.slice(3, 6)}-${d.slice(6)}`;
  return digits;
}

export const ORDER_STATUS_LABEL: Record<string, string> = {
  pending: "결제 대기",
  paid: "결제 완료",
  picked_up: "찾아감",
  cancelled: "취소",
  failed: "결제 실패",
};

/** "HH:MM" 형식만 받는다 (제조 시각 입력) */
export const isClock = (v: string) => /^([01]\d|2[0-3]):[0-5]\d$/.test(v);

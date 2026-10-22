// 토스페이먼츠 결제 승인 호출 (서버 전용 — 브라우저 코드에서 가져오지 않는다).
// 기본값은 토스 공식 문서의 공개 테스트 시크릿 키(결제위젯 gsk)다. 실제 돈이 오가지 않는다.
// 운영 전환 때 Vercel 환경변수 TOSS_SECRET_KEY를 live 키로 바꾼다.
const TOSS_SECRET_KEY = process.env.TOSS_SECRET_KEY?.trim() || "test_gsk_docs_OaPz8L5KdmQXkzRz3y47BMw6";

export type ConfirmInput = { paymentKey: string; orderId: string; amount: number };
export type ConfirmResult = { ok: true; approvedAt: string | null; method: string | null } | { ok: false; code: string; message: string };

/** 토스 결제 승인 API. 금액 대조는 호출 전에 반드시 서버에서 끝낸다. */
export async function confirmPayment(input: ConfirmInput, fetchImpl: typeof fetch = fetch, secretKey = TOSS_SECRET_KEY): Promise<ConfirmResult> {
  const res = await fetchImpl("https://api.tosspayments.com/v1/payments/confirm", {
    method: "POST",
    headers: {
      Authorization: `Basic ${Buffer.from(`${secretKey}:`).toString("base64")}`,
      "Content-Type": "application/json",
      "Idempotency-Key": `confirm-${input.orderId}`,
    },
    body: JSON.stringify(input),
  });
  const data = (await res.json().catch(() => ({}))) as Record<string, unknown>;
  if (!res.ok) return { ok: false, code: String(data.code ?? res.status), message: String(data.message ?? "결제 승인에 실패했어요.") };
  return { ok: true, approvedAt: (data.approvedAt as string) ?? null, method: (data.method as string) ?? null };
}

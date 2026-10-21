import { describe, expect, it, vi } from "vitest";
import { confirmPayment } from "./toss";

const input = { paymentKey: "pk_1", orderId: "OD-20261021-abc123", amount: 13900 };

describe("confirmPayment", () => {
  it("시크릿 키를 Basic 인증으로 보내고 승인 결과를 돌려준다", async () => {
    const fetchMock = vi.fn(async () => new Response(JSON.stringify({ approvedAt: "2026-10-21T19:00:00+09:00", method: "카드" }), { status: 200 }));
    const r = await confirmPayment(input, fetchMock as unknown as typeof fetch, "test_gsk_x");
    expect(r).toEqual({ ok: true, approvedAt: "2026-10-21T19:00:00+09:00", method: "카드" });
    const [url, init] = fetchMock.mock.calls[0] as unknown as [string, RequestInit];
    expect(url).toBe("https://api.tosspayments.com/v1/payments/confirm");
    expect((init.headers as Record<string, string>).Authorization).toBe(`Basic ${Buffer.from("test_gsk_x:").toString("base64")}`);
    expect(JSON.parse(String(init.body))).toEqual(input);
  });

  it("토스 오류 코드를 그대로 전달한다", async () => {
    const fetchMock = vi.fn(async () => new Response(JSON.stringify({ code: "REJECT_CARD_COMPANY", message: "카드사 거절" }), { status: 400 }));
    expect(await confirmPayment(input, fetchMock as unknown as typeof fetch, "k")).toEqual({ ok: false, code: "REJECT_CARD_COMPANY", message: "카드사 거절" });
  });
});

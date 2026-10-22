// Supabase 공개 접속 정보. publishable 키는 브라우저에 공개되도록 만든 키라 코드에 기본값을 둔다.
// 비밀 키는 사이트에 두지 않는다. 주문·결제는 Supabase 함수 "orders"가 Supabase 안의 키로 처리한다.
export const SUPABASE_URL = process.env.NEXT_PUBLIC_SUPABASE_URL ?? "https://dvbluucydlzkfpzcjmea.supabase.co";
export const SUPABASE_PUBLISHABLE_KEY =
  process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY ?? "sb_publishable_5bjJdcMLFqYdSher-FxxfA_AuRgXw36";

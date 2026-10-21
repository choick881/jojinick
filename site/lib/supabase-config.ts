// Supabase 공개 접속 정보. publishable 키는 브라우저에 공개되도록 만든 키라 코드에 기본값을 둔다.
// 비밀 키(SUPABASE_SECRET_KEY)는 서버 환경변수로만 받고, 여기에 두지 않는다.
export const SUPABASE_URL = process.env.NEXT_PUBLIC_SUPABASE_URL ?? "https://dvbluucydlzkfpzcjmea.supabase.co";
export const SUPABASE_PUBLISHABLE_KEY =
  process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY ?? "sb_publishable_5bjJdcMLFqYdSher-FxxfA_AuRgXw36";

// supabase/functions/orders 를 lib/ 코드와 함께 한 파일로 묶는다(Supabase 함수 배포용).
// 결과: supabase/functions/orders/.build/index.ts (저장소에는 올리지 않음)
import { build } from "esbuild";

await build({
  entryPoints: ["supabase/functions/orders/index.ts"],
  outfile: "supabase/functions/orders/.build/index.ts",
  bundle: true,
  format: "esm",
  platform: "neutral",
  target: "es2022",
  external: ["npm:*"],
  // lib/toss.ts가 읽는 Node 환경변수: 함수에서는 Deno.env로 따로 넘긴다
  define: { "process.env.TOSS_SECRET_KEY": "undefined" },
  banner: { js: "// 자동 생성 파일(npm run build:edge). 직접 고치지 말고 lib/·supabase/functions/orders/index.ts를 고친다." },
  logLevel: "warning",
});
console.log("built supabase/functions/orders/.build/index.ts");

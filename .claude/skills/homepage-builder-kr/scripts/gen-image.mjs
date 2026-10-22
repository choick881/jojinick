#!/usr/bin/env node
// GPT image generation CLI for homepage-builder-kr (no dependencies, Node >= 18).
// Text-to-image:  POST /v1/images/generations
// With --ref:     POST /v1/images/edits (reference images guide the result)
import { spawnSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { parseArgs } from "node:util";

// Node's built-in fetch ignores HTTPS_PROXY unless NODE_USE_ENV_PROXY=1 (Node >= 22.21).
// Re-exec once with it set so the script works behind proxies (e.g. cloud sandboxes).
const proxy = process.env.HTTPS_PROXY || process.env.https_proxy;
if (proxy && !process.env.NODE_USE_ENV_PROXY) {
  const r = spawnSync(process.execPath, ["--disable-warning=UNDICI-EHPA", ...process.argv.slice(1)], {
    stdio: "inherit",
    env: { ...process.env, NODE_USE_ENV_PROXY: "1" },
  });
  process.exit(r.status ?? 1);
}

const HELP = `사용법: node gen-image.mjs --prompt "<프롬프트>" [옵션]

  --prompt <text>        이미지 프롬프트 (또는 --prompt-file)
  --prompt-file <path>   프롬프트를 파일에서 읽기
  --name <basename>      저장 파일 이름 (기본: img-<시각>)
  --out <dir>            저장 폴더 (기본: brand/images)
  --size <WxH|auto>      1024x1024 | 1536x1024 | 1024x1536 | auto (기본 1024x1024)
  --quality <q>          low | medium | high | auto (기본 high)
  --n <1-10>             생성 개수 (기본 1)
  --format <f>           png | jpeg | webp (기본 png)
  --model <id>           기본 gpt-image-2 (환경변수 OPENAI_IMAGE_MODEL로 변경 가능)
  --ref <path>           참고 이미지 (여러 번 지정 가능) → 편집/변형 모드
  --log <path>           프롬프트 기록 파일 (기본: brand/prompts.jsonl)
  --dry-run              API를 호출하지 않고 요청 내용만 출력
  -h, --help             도움말

필요 조건: 환경변수 OPENAI_API_KEY, api.openai.com 네트워크 접근`;

const { values: opt } = parseArgs({
  options: {
    prompt: { type: "string" },
    "prompt-file": { type: "string" },
    name: { type: "string" },
    out: { type: "string", default: "brand/images" },
    size: { type: "string", default: "1024x1024" },
    quality: { type: "string", default: "high" },
    n: { type: "string", default: "1" },
    format: { type: "string", default: "png" },
    model: { type: "string", default: process.env.OPENAI_IMAGE_MODEL || "gpt-image-2" },
    ref: { type: "string", multiple: true, default: [] },
    log: { type: "string", default: "brand/prompts.jsonl" },
    "dry-run": { type: "boolean", default: false },
    help: { type: "boolean", short: "h", default: false },
  },
});

function fail(msg) {
  console.error(`오류: ${msg}`);
  process.exit(1);
}

if (opt.help) {
  console.log(HELP);
  process.exit(0);
}

const prompt = opt["prompt-file"] ? fs.readFileSync(opt["prompt-file"], "utf8").trim() : opt.prompt?.trim();
if (!prompt) fail("--prompt 또는 --prompt-file이 필요합니다. --help 참고");

const n = Number(opt.n);
if (!Number.isInteger(n) || n < 1 || n > 10) fail("--n은 1~10 사이 정수여야 합니다");
if (!["low", "medium", "high", "auto"].includes(opt.quality)) fail("--quality는 low|medium|high|auto");
if (!["png", "jpeg", "webp"].includes(opt.format)) fail("--format은 png|jpeg|webp");
if (opt.size !== "auto") {
  const m = /^(\d+)x(\d+)$/.exec(opt.size);
  if (!m) fail("--size는 1024x1024 형식 또는 auto");
  const [w, h] = [Number(m[1]), Number(m[2])];
  if (w % 16 || h % 16) fail("--size의 가로·세로는 16의 배수여야 합니다");
}
for (const r of opt.ref) if (!fs.existsSync(r)) fail(`참고 이미지가 없습니다: ${r}`);

const mode = opt.ref.length ? "edits" : "generations";
const baseName = opt.name || `img-${new Date().toISOString().replace(/[-:T]/g, "").slice(0, 14)}`;
const request = { model: opt.model, prompt, n, size: opt.size, quality: opt.quality, output_format: opt.format };

if (opt["dry-run"]) {
  console.log(JSON.stringify({ endpoint: `/v1/images/${mode}`, ...request, refs: opt.ref }, null, 2));
  process.exit(0);
}

const apiKey = process.env.OPENAI_API_KEY;
if (!apiKey) {
  fail(
    "OPENAI_API_KEY 환경변수가 없습니다.\n" +
      "  - 로컬: export OPENAI_API_KEY=... 후 다시 실행\n" +
      "  - Claude Code 클라우드: 환경 설정 → 환경변수에 추가하고 새 세션 시작",
  );
}

const MIME = { ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp" };

async function callApi() {
  const url = `https://api.openai.com/v1/images/${mode}`;
  const headers = { Authorization: `Bearer ${apiKey}` };
  if (mode === "generations") {
    return fetch(url, { method: "POST", headers: { ...headers, "Content-Type": "application/json" }, body: JSON.stringify(request) });
  }
  const form = new FormData();
  for (const [k, v] of Object.entries(request)) form.append(k, String(v));
  for (const r of opt.ref) {
    const type = MIME[path.extname(r).toLowerCase()] || "image/png";
    form.append("image[]", new Blob([fs.readFileSync(r)], { type }), path.basename(r));
  }
  return fetch(url, { method: "POST", headers, body: form });
}

let res;
try {
  res = await callApi();
} catch (err) {
  fail(
    `api.openai.com에 연결하지 못했습니다 (${err.cause?.code || err.message}).\n` +
      "  클라우드 환경이라면 Network access의 Allowed domains에 api.openai.com을 추가하세요.",
  );
}

const body = await res.json().catch(() => ({}));
if (!res.ok) fail(`OpenAI API ${res.status}: ${body.error?.message || JSON.stringify(body)}`);

fs.mkdirSync(opt.out, { recursive: true });
const files = (body.data || []).map((d, i) => {
  const file = path.join(opt.out, n > 1 ? `${baseName}-${i + 1}.${opt.format}` : `${baseName}.${opt.format}`);
  fs.writeFileSync(file, Buffer.from(d.b64_json, "base64"));
  return file;
});
if (!files.length) fail(`응답에 이미지가 없습니다: ${JSON.stringify(body).slice(0, 300)}`);

fs.mkdirSync(path.dirname(opt.log), { recursive: true });
fs.appendFileSync(
  opt.log,
  JSON.stringify({ ts: new Date().toISOString(), mode, ...request, refs: opt.ref, files, usage: body.usage }) + "\n",
);

for (const f of files) console.log(f);

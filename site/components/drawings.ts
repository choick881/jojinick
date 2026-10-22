// 사진 자리 선 그림 (prototypes/src/partials/ph-*.svg와 같은 그림). 사진이 생기면 PhotoSlot의 src로 대체된다.
export const DRAWINGS = {
  bowl: `<path d="M30 40h60c0 16-13 26-30 26S30 56 30 40z"/><path d="M24 40h72"/><path d="M52 30c-4-4 4-7 0-12M68 30c-4-4 4-7 0-12"/>`,
  boxes: `<rect x="12" y="20" width="28" height="22" rx="4"/><rect x="46" y="20" width="28" height="22" rx="4"/><rect x="80" y="20" width="28" height="22" rx="4"/><rect x="12" y="48" width="28" height="22" rx="4"/><rect x="46" y="48" width="28" height="22" rx="4"/><rect x="80" y="48" width="28" height="22" rx="4"/><circle cx="26" cy="26" r="2"/><circle cx="60" cy="26" r="2"/><circle cx="94" cy="26" r="2"/>`,
  locker: `<rect x="22" y="6" width="76" height="68" rx="4"/><path d="M22 28h76M22 50h76M47 6v68M72 6v68"/>`,
  person: `<circle cx="60" cy="30" r="14"/><path d="M30 74c4-18 16-26 30-26s26 8 30 26"/>`,
  pot: `<path d="M28 34h64v24a12 12 0 0 1-12 12H40a12 12 0 0 1-12-12z"/><path d="M20 34h80M50 24c-4-4 4-7 0-12M70 24c-4-4 4-7 0-12"/>`,
  shop: `<path d="M10 70h100M20 70V30l40-18 40 18v40"/><rect x="50" y="44" width="20" height="26"/><rect x="28" y="40" width="14" height="12"/><rect x="78" y="40" width="14" height="12"/>`,
  table: `<ellipse cx="60" cy="52" rx="56" ry="22"/><circle cx="40" cy="44" r="11"/><circle cx="70" cy="40" r="13"/><circle cx="92" cy="54" r="8"/><circle cx="56" cy="62" r="8"/><path d="M68 22c-3-3 3-5 0-9M74 22c-3-3 3-5 0-9"/>`,
  tray: `<rect x="14" y="14" width="92" height="56" rx="8"/><circle cx="38" cy="36" r="10"/><circle cx="72" cy="36" r="12"/><circle cx="38" cy="56" r="6"/><circle cx="60" cy="58" r="6"/><circle cx="82" cy="58" r="6"/>`,
} as const;
export type Drawing = keyof typeof DRAWINGS;

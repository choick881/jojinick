import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";
import { notFound } from "next/navigation";
import { Faq, HOW_TO, Promises, STAGED_NOTE, SectionHead, Steps } from "@/components/blocks";
import { BuyBox } from "@/components/buy-box";
import { PhotoSlot } from "@/components/photo-slot";
import { categoryName, getProduct, getProducts, getStoreStatus, HEATING, type Product } from "@/lib/catalog";
import { won } from "@/lib/price";
import { absoluteUrl, jsonLd } from "@/lib/site";

export function generateStaticParams() {
  return getProducts().map((p) => ({ slug: p.slug }));
}

export async function generateMetadata({ params }: PageProps<"/menu/[slug]">): Promise<Metadata> {
  const p = getProduct((await params).slug);
  if (!p) return {};
  const description = `${p.name} ${won(p.price)} · ${p.size}. 오늘 아침 만들어 미리 결제하고 퇴근길에 찾아가세요.`;
  return { title: p.name, description, alternates: { canonical: `/menu/${p.slug}` }, openGraph: { title: `${p.name} · 온담찬`, description } };
}

const FAQ = [
  { q: "무인 매장인데 어떻게 찾아가나요?", a: "결제하면 문자로 주문번호가 옵니다. 고르신 시간에 매장 픽업 냉장고에서 주문번호가 붙은 봉투를 꺼내 가시면 됩니다. 부모님이 대신 찾아가실 때는 '받는 분' 성함으로 확인하세요." },
  { q: "얼마나 보관할 수 있나요?", a: "찾아가신 날 드시는 것이 가장 맛있습니다. 냉장(0~10℃)에 두시고, 용기 라벨의 소비기한 안에 드세요." },
  { q: "픽업 시간을 놓치면 어떻게 되나요?", a: "그날 매장 마감(23:00) 전까지는 픽업 냉장고에 보관해 둡니다. 마감 뒤에는 위생을 위해 폐기하며 환불은 어렵습니다. (운영 정책 확정 전 예시)" },
  { q: "어떻게 데우면 되나요?", a: "국은 냄비에서 중불로 3~4분, 메인찬은 전자레인지 700W로 1분 30초 데워 주세요. 나물과 볶음 반찬은 그대로 드시면 됩니다." },
];

function heatingSteps(p: Product) {
  if (p.components?.length) {
    const roles = new Set(p.components.map((c) => c.role));
    const steps = [];
    if (roles.has("국")) steps.push({ title: "국은 냄비에", body: HEATING.soup });
    if (roles.has("메인찬")) steps.push({ title: "메인찬은 전자레인지에", body: HEATING.main });
    steps.push({ title: "반찬은 그대로", body: "나물과 볶음, 부드러운 반찬은 데우지 않고 바로 드세요." });
    return steps;
  }
  return [{ title: categoryName(p.category), body: HEATING[p.category] ?? HEATING.basic }];
}

export default async function ProductPage({ params }: PageProps<"/menu/[slug]">) {
  const p = getProduct((await params).slug);
  if (!p) notFound();
  const status = getStoreStatus();
  const isSet = Boolean(p.components?.length);
  const firstItem = p.components?.[0];
  const heat = heatingSteps(p);

  const productLd = {
    "@context": "https://schema.org",
    "@type": "Product",
    name: p.name,
    description: p.size,
    category: categoryName(p.category),
    brand: { "@type": "Brand", name: "온담찬" },
    offers: {
      "@type": "Offer",
      price: p.price,
      priceCurrency: "KRW",
      availability: p.soldOut ? "https://schema.org/OutOfStock" : "https://schema.org/InStock",
      url: absoluteUrl(`/menu/${p.slug}`),
    },
  };

  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: jsonLd(productLd) }} />
      {/* 1. 구매 영역 */}
      <section className="gut pb-12 pt-6">
        <div className="wrap grid gap-6 md:grid-cols-[1.1fr_1fr] md:items-start md:gap-10">
          <div className="min-w-0">
            <PhotoSlot drawing={isSet ? "table" : "bowl"} caption={`${p.name} (45° 자연광)`} ratio="4 / 5" />
            <p className="staged mt-1.5">{STAGED_NOTE}</p>
          </div>
          <div className="grid min-w-0 gap-4.5">
            <span className="hand">오늘 아침에 만들었어요</span>
            <div className="flex flex-wrap gap-1.5">
              {p.featured && <span className="rounded-full bg-accent px-2.5 py-0.5 text-[.72rem] font-bold text-white">대표 상품</span>}
              <span className="rounded-full bg-sand px-2.5 py-0.5 text-[.72rem] font-bold text-brand">{categoryName(p.category)}</span>
              <span className="rounded-full bg-sand px-2.5 py-0.5 text-[.72rem] font-bold text-brand">매장 픽업</span>
              {p.softness && <span className="rounded-full bg-sand px-2.5 py-0.5 text-[.72rem] font-bold text-brand">부드러움: {p.softness}</span>}
            </div>
            <div className="grid gap-1.5">
              <h1 className="title text-[1.8rem]">{p.name}</h1>
              <p className="text-muted">{p.size}</p>
            </div>
            <div className="flex items-baseline gap-2"><b className="num text-[1.75rem] font-extrabold">{won(p.price)}</b></div>
            {/* B안 요약표 */}
            <div className="summary" aria-label="요약">
              <div><small>만든 시각{status.isExample && " (예시)"}</small><b className="num">오전 {status.madeAt}</b></div>
              <div><small>픽업</small><b className="num">17:30~20:30</b></div>
              <div><small>보관</small><b>냉장</b></div>
            </div>
            <BuyBox slug={p.slug} name={p.name} price={p.price} soldOut={p.soldOut} />
            <p className="rounded-[10px] border border-dashed border-line bg-white px-3 py-2.5 text-[.85rem] text-muted">
              <b className="text-ink">부모님께 보내시나요?</b> 결제할 때 &lsquo;받는 분&rsquo;에 부모님 성함을 적으면, 부모님이 그 이름으로 직접 찾아가실 수 있어요.
            </p>
          </div>
        </div>
      </section>

      {/* 2. 후킹 */}
      <section className="gut sec sec-alt text-center">
        <div className="narrow grid justify-items-center gap-2.5">
          <span className="eyebrow">퇴근길 저녁</span>
          <h2 className="h2">퇴근길, 오늘 저녁이<br />준비되어 있어요</h2>
          <p className="lead">아침에 끓인 국과 반찬을 1인분씩 담아 둡니다. 미리 결제하고, 원하는 시간에 찾아가 데우기만 하세요.</p>
        </div>
      </section>

      {/* 3. 구성 */}
      {isSet && (
        <section className="gut sec">
          <div className="narrow">
            <SectionHead eyebrow="오늘의 구성" title={<>한 끼에 필요한 만큼만,<br />{p.components!.length}가지를 담았어요</>} />
            <PhotoSlot drawing="boxes" caption="용기 탑뷰 (크림 바탕)" ratio="3 / 2" />
            <ul className="mt-5 grid grid-cols-2 gap-3 md:grid-cols-4">
              {p.components!.map((c, i) => (
                <li key={i} className="card grid gap-1 p-3.5">
                  <small className="text-[.72rem] font-bold text-brand">{c.role}</small>
                  <b className="text-[.95rem]">{c.name}</b>
                  <span className="num text-[.82rem] text-muted">{c.amount}</span>
                </li>
              ))}
            </ul>
            <p className="mt-2.5 text-[.82rem] text-muted">구성은 그날 만든 반찬에 따라 바뀝니다. 밥은 들어 있지 않아요.</p>
          </div>
        </section>
      )}

      {/* 4. 약속 */}
      <section className={`gut sec ${isSet ? "sec-alt" : ""}`}>
        <div className="narrow"><SectionHead eyebrow="온담찬의 약속" title="숫자로 말씀드릴게요" /><Promises /></div>
      </section>

      {/* 5. 제조시간 라벨 */}
      <section className="gut sec">
        <div className="narrow grid items-center gap-6 md:grid-cols-2">
          <div className="grid gap-2.5">
            <span className="eyebrow">제조시간 라벨</span>
            <h2 className="h2">언제 만들었는지,<br />숨기지 않습니다</h2>
            <ul className="grid gap-2.5">
              {["모든 용기에 만든 날짜와 시각을 분 단위로 적어요.", "소비기한과 보관 온도를 같은 라벨에 함께 적어요.", "주홍 칸만 보시면 됩니다. 오늘 아침 숫자인지 확인하세요."].map((t) => (
                <li key={t} className="grid grid-cols-[18px_1fr] items-start gap-2"><span className="mt-[.6em] size-2.5 rounded-full bg-accent" aria-hidden="true" />{t}</li>
              ))}
            </ul>
          </div>
          <div role="img" aria-label={`제조시간 라벨 예시: ${firstItem?.name ?? p.name}, 제조 오전 ${status.madeAt}`}
            className="grid w-full max-w-[360px] -rotate-[1.5deg] gap-3 justify-self-center rounded-2xl bg-white px-5.5 pb-4.5 pt-5.5 shadow-[0_1px_0_var(--line),0_10px_30px_rgba(43,33,26,.1)]">
            <div className="flex items-center justify-between gap-2.5 border-b-2 border-ink pb-2.5">
              <Image src="/brand/symbol.svg" alt="" width={26} height={26} />
              <span className="text-[13px] font-bold text-brand">온담찬 · 양주</span>
            </div>
            <h3 className="text-[24px] font-extrabold">{firstItem?.name ?? p.name}</h3>
            <div className="flex items-baseline justify-between rounded-[10px] border-2 border-accent bg-[#FFF4EC] px-3 py-2.5">
              <span className="text-[14px] font-bold text-accent-deep">제조</span><b className="num text-[26px] font-extrabold">10.21 {status.madeAt}</b>
            </div>
            <dl className="grid grid-cols-[auto_1fr] gap-x-3.5 gap-y-1.5 text-[15px]">
              <dt className="text-muted">내용량</dt><dd className="num font-bold">{firstItem?.amount ?? p.size}</dd>
              <dt className="text-muted">소비기한</dt><dd className="num font-bold">10.22 까지</dd>
              <dt className="text-muted">보관</dt><dd className="font-bold">냉장 0~10℃</dd>
            </dl>
            <p className="text-[11.5px] leading-normal text-muted">라벨 예시입니다. 소비기한과 알레르기 표시는 품목별 기준을 확정한 뒤 적습니다.</p>
          </div>
        </div>
      </section>

      {/* 6. 데우는 법 */}
      <section className="gut sec sec-alt">
        <div className="narrow">
          <SectionHead eyebrow="맛있게 드시는 법" title={<>데우기만 하면<br />저녁 준비 끝</>} />
          <Steps items={heat} />
        </div>
      </section>

      {/* 7. 정보 고시 */}
      <section className="gut sec">
        <div className="narrow">
          <SectionHead eyebrow="상품 정보 고시" title="상품 정보" />
          <div className="overflow-x-auto rounded-xl border border-line">
            <table className="w-full border-collapse bg-white text-[.85rem]">
              <tbody className="[&_td]:border-b [&_td]:border-line [&_td]:px-3.5 [&_td]:py-2.5 [&_th]:w-[34%] [&_th]:border-b [&_th]:border-line [&_th]:bg-[#FAF5EB] [&_th]:px-3.5 [&_th]:py-2.5 [&_th]:text-left [&_th]:align-top [&_th]:font-medium [&_th]:text-muted [&_tr:last-child>*]:border-0">
                <tr><th>제품명</th><td>{p.name}</td></tr>
                <tr><th>식품 유형</th><td>반찬류<span className="todo">사업자 확인 필요</span></td></tr>
                <tr><th>내용량</th><td className="num">{p.size}</td></tr>
                <tr><th>원재료명 및 원산지</th><td>{p.ingredients || p.origin ? `${p.ingredients} ${p.origin}` : <>품목별 표기<span className="todo">사업자 확인 필요</span></>}</td></tr>
                <tr><th>알레르기 유발 물질</th><td>{p.allergens || <>품목별 표기<span className="todo">사업자 확인 필요</span></>}</td></tr>
                <tr><th>제조일시 · 소비기한</th><td>용기 라벨에 표기</td></tr>
                <tr><th>보관 방법</th><td>냉장 보관 (0~10℃)</td></tr>
                <tr><th>제조 · 판매</th><td>온담찬 · 경기도 양주시<span className="todo">주소 확인 필요</span></td></tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>

      {/* 8. 픽업 안내 */}
      <section className="gut sec sec-alt">
        <div className="narrow">
          <SectionHead eyebrow="픽업 안내" title={<>무인 매장에서<br />이렇게 찾아가세요</>} />
          <Steps items={HOW_TO} />
          <p className="mt-3 text-[.85rem] text-muted">취소는 픽업 3시간 전까지 할 수 있어요. 그 뒤에는 이미 만든 음식이라 취소가 어려워요. (정책 예시) <Link href="/policy/refund" className="underline underline-offset-4">환불 정책</Link></p>
        </div>
      </section>

      {/* 9. FAQ */}
      <section className="gut sec">
        <div className="narrow"><SectionHead eyebrow="자주 묻는 질문" title="궁금한 점" /><Faq items={FAQ} /></div>
      </section>

      {/* 10. 마무리 */}
      <section className="gut sec sec-alt pb-28 md:pb-16">
        <div className="narrow grid justify-items-center gap-4 text-center">
          <span className="hand">오늘 저녁은 온담찬에서</span>
          <h2 className="h2">매일의 식사에<br />온기를 담다</h2>
          <p className="lead">{p.name} <b className="num">{won(p.price)}</b> · 17:30부터 픽업</p>
          <Link href="/menu" className="btn btn-ghost">다른 메뉴 보기</Link>
        </div>
      </section>
    </>
  );
}

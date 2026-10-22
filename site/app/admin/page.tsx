import type { Metadata } from "next";
import { Suspense } from "react";
import { markPickedUp, setSoldOut, signOut } from "./actions";
import { AutoRefresh } from "@/components/admin/auto-refresh";
import { LoginForm } from "@/components/admin/login-form";
import { MadeAtForm } from "@/components/admin/made-at-form";
import { ORDER_STATUS_LABEL, formatPhone, kstDate } from "@/lib/admin";
import { won } from "@/lib/price";
import { getAdmin } from "@/lib/supabase/server";

export const metadata: Metadata = { title: "관리자", robots: { index: false, follow: false } };

type OrderRow = {
  id: string;
  order_number: string;
  customer_name: string;
  customer_phone: string;
  recipient_name: string | null;
  recipient_phone: string | null;
  pickup_date: string;
  pickup_time: string;
  total_amount: number;
  status: string;
  order_items: { product_name: string; quantity: number }[];
};

export default function AdminPage() {
  return (
    <section className="gut pt-9 pb-18">
      <div className="wrap grid gap-5">
        <Suspense fallback={<p className="lead">불러오는 중…</p>}>
          <AdminBody />
        </Suspense>
      </div>
    </section>
  );
}

async function AdminBody() {
  const { db, email, isAdmin } = await getAdmin();
  if (!email) return <LoginForm />;
  if (!isAdmin)
    return (
      <div className="card mx-auto grid max-w-sm gap-3 p-6 text-center">
        <p className="lead">{email} 계정은 관리자로 등록되어 있지 않아요.</p>
        <form action={signOut}><button className="btn btn-ghost w-full">로그아웃</button></form>
      </div>
    );

  const now = new Date();
  const days = [kstDate(now), kstDate(now, 1)];
  const [status, products, orders] = await Promise.all([
    db.from("store_status").select("made_at").eq("id", 1).maybeSingle(),
    db.from("products").select("slug, name, category, sold_out, is_active").order("sort"),
    db
      .from("orders")
      .select("id, order_number, customer_name, customer_phone, recipient_name, recipient_phone, pickup_date, pickup_time, total_amount, status, order_items(product_name, quantity)")
      .in("pickup_date", days)
      .in("status", ["paid", "picked_up"])
      .order("pickup_date")
      .order("pickup_time")
      .returns<OrderRow[]>(),
  ]);
  const madeAt = status.data?.made_at?.slice(0, 5) ?? "07:00";
  const list = orders.data ?? [];
  const waiting = list.filter((o) => o.pickup_date === days[0] && o.status === "paid").length;

  return (
    <>
      <AutoRefresh seconds={60} />
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div className="grid gap-1"><span className="eyebrow">관리자</span><h1 className="title text-[clamp(1.6rem,4vw,2.1rem)]">오늘의 가게</h1></div>
        <form action={signOut} className="flex items-center gap-3 text-[.85rem] text-muted">{email}<button className="btn btn-ghost min-h-11">로그아웃</button></form>
      </div>

      <div className="card grid gap-3 p-5">
        <h2 className="text-[1.15rem] font-extrabold">오늘 찾아갈 주문 <span className="num text-accent-deep">{waiting}건</span></h2>
        <p className="text-[.82rem] text-muted">1분마다 새로 고칩니다. 결제가 끝난 주문만 보입니다.</p>
      </div>

      {days.map((day, i) => {
        const dayOrders = list.filter((o) => o.pickup_date === day);
        return (
          <div key={day} className="card grid gap-3 p-5">
            <h2 className="text-[1.15rem] font-extrabold">{i === 0 ? "오늘" : "내일"} 주문 <span className="num text-[.9rem] font-normal text-muted">{day} · {dayOrders.length}건</span></h2>
            {dayOrders.length === 0 ? (
              <p className="text-[.9rem] text-muted">주문이 없어요.</p>
            ) : (
              <ul className="grid gap-2.5">
                {dayOrders.map((o) => (
                  <li key={o.id} className={`grid gap-1.5 rounded-[12px] border border-line p-3.5 ${o.status === "picked_up" ? "opacity-55" : ""}`}>
                    <div className="flex flex-wrap items-baseline justify-between gap-2">
                      <b className="num text-[1.2rem] text-brand">{o.pickup_time.slice(0, 5)}</b>
                      <span className="text-[.8rem] font-bold">{ORDER_STATUS_LABEL[o.status] ?? o.status}</span>
                    </div>
                    <p className="text-[.95rem]">{o.order_items.map((it) => `${it.product_name} ×${it.quantity}`).join(", ")}</p>
                    <p className="text-[.85rem] text-muted">
                      주문 {o.customer_name} <span className="num">{formatPhone(o.customer_phone)}</span>
                      {o.recipient_name && <> · 받는 분 <b className="text-ink">{o.recipient_name}</b> <span className="num">{formatPhone(o.recipient_phone ?? "")}</span></>}
                    </p>
                    <div className="flex flex-wrap items-center justify-between gap-2 text-[.8rem] text-muted">
                      <span className="num">{o.order_number} · {won(o.total_amount)}</span>
                      {o.status === "paid" && (
                        <form action={markPickedUp.bind(null, o.id)}><button className="btn btn-ghost min-h-10 px-4 text-[.85rem]">찾아감 표시</button></form>
                      )}
                    </div>
                  </li>
                ))}
              </ul>
            )}
          </div>
        );
      })}

      <div className="card grid gap-3 p-5">
        <h2 className="text-[1.15rem] font-extrabold">매장 현황판</h2>
        <MadeAtForm current={madeAt} />
        <p className="text-[.8rem] text-muted">홈 화면의 &ldquo;오늘 만든 시각&rdquo;에 바로 반영됩니다.</p>
      </div>

      <div className="card grid gap-3 p-5">
        <h2 className="text-[1.15rem] font-extrabold">품절 관리</h2>
        <p className="text-[.8rem] text-muted">누르면 바로 메뉴 화면에 반영됩니다. 품절 상품은 주문할 수 없어요.</p>
        <ul className="grid gap-2 sm:grid-cols-2">
          {(products.data ?? []).filter((p) => p.is_active).map((p) => (
            <li key={p.slug} className="flex items-center justify-between gap-2 rounded-[10px] border border-line px-3 py-2">
              <span className={p.sold_out ? "text-muted line-through" : ""}>{p.name}</span>
              <form action={setSoldOut.bind(null, p.slug, !p.sold_out)}>
                <button className={`chip min-w-24 ${p.sold_out ? "" : "border-brand text-brand"}`} aria-pressed={p.sold_out}>{p.sold_out ? "품절" : "판매 중"}</button>
              </form>
            </li>
          ))}
        </ul>
      </div>
    </>
  );
}

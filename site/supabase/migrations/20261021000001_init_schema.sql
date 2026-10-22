-- 온담찬 초기 스키마: 상품·분류·매장 현황·픽업 시간대·주문·관리자
-- 원칙: 주문(개인정보)은 anon/일반 로그인 사용자에게 열지 않는다. 주문 생성·조회는 서버(secret key)와 관리자만.

-- 관리자 판별은 API로 노출되지 않는 private 스키마에 둔다
create schema if not exists private;

create table public.categories (
  slug text primary key,
  name text not null,
  sort integer not null default 0
);

create table public.products (
  id uuid primary key default gen_random_uuid(),
  slug text unique not null,
  category text not null references public.categories(slug),
  name text not null,
  price integer not null check (price >= 0),          -- 원화 정수
  size text not null default '',
  featured boolean not null default false,
  softness text check (softness in ('씹기 쉬움', '잇몸으로', '혀로')),
  ingredients text not null default '',
  origin text not null default '',
  allergens text not null default '',
  components jsonb,                                     -- 세트 구성 [{role,name,amount}]
  sort integer not null default 0,
  is_active boolean not null default true,              -- 판매 목록에 보이는지
  sold_out boolean not null default false,              -- 오늘 품절
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
create index products_category_idx on public.products (category);

-- 매장 현황판: 한 줄짜리 표
create table public.store_status (
  id smallint primary key default 1 check (id = 1),
  made_at time not null default '07:00',               -- 오늘 아침 제조 시각
  updated_at timestamptz not null default now()
);

-- 픽업 시간대와 시간대별 최대 주문 수
create table public.pickup_slots (
  time text primary key check (time ~ '^[0-2][0-9]:[0-5][0-9]$'),
  capacity integer not null default 20 check (capacity >= 0),
  is_active boolean not null default true
);

create table public.orders (
  id uuid primary key default gen_random_uuid(),
  order_number text unique not null check (order_number ~ '^[A-Za-z0-9_-]{6,64}$'),  -- 토스 orderId
  order_name text not null,                             -- "1인 저녁세트 외 2건"
  customer_name text not null,
  customer_phone text not null,
  recipient_name text,                                  -- 부모님 등 받는 분 (없으면 주문자)
  recipient_phone text,
  fulfillment_type text not null default 'pickup' check (fulfillment_type in ('pickup', 'local_delivery', 'parcel')),
  pickup_date date,
  pickup_time text references public.pickup_slots(time),
  address_line text,                                    -- 배달·택배용 (스위치 OFF 동안 비어 있음)
  address_detail text,
  postal_code text,
  total_amount integer not null check (total_amount >= 0),   -- 서버가 계산한 금액
  status text not null default 'pending' check (status in ('pending', 'paid', 'picked_up', 'cancelled', 'failed')),
  toss_payment_key text,
  paid_at timestamptz,
  memo text,
  created_at timestamptz not null default now()
);
create index orders_pickup_idx on public.orders (pickup_date, pickup_time);
create index orders_status_idx on public.orders (status);

create table public.order_items (
  id uuid primary key default gen_random_uuid(),
  order_id uuid not null references public.orders(id) on delete cascade,
  product_id uuid not null references public.products(id),
  product_name text not null,                           -- 주문 시점 이름·가격 스냅샷
  unit_price integer not null check (unit_price >= 0),
  quantity integer not null check (quantity > 0)
);
create index order_items_order_idx on public.order_items (order_id);
create index order_items_product_idx on public.order_items (product_id);

-- 관리자 허용 목록 (Supabase Auth 이메일)
create table public.admin_users (
  email text primary key
);

create function private.is_admin() returns boolean
language sql stable security definer set search_path = ''
as $$
  select exists (select 1 from public.admin_users a where a.email = (auth.jwt() ->> 'email'));
$$;
grant usage on schema private to authenticated;
grant execute on function private.is_admin() to authenticated;

create function private.touch_updated_at() returns trigger
language plpgsql set search_path = ''
as $$ begin new.updated_at := now(); return new; end; $$;
create trigger products_touch before update on public.products for each row execute function private.touch_updated_at();
create trigger store_status_touch before update on public.store_status for each row execute function private.touch_updated_at();

-- RLS
alter table public.categories enable row level security;
alter table public.products enable row level security;
alter table public.store_status enable row level security;
alter table public.pickup_slots enable row level security;
alter table public.orders enable row level security;
alter table public.order_items enable row level security;
alter table public.admin_users enable row level security;

-- 누구나 읽기: 분류, 판매 중 상품, 현황판, 픽업 시간대
create policy "public reads categories" on public.categories for select to anon, authenticated using (true);
create policy "public reads active products" on public.products for select to anon, authenticated using (is_active);  -- 관리자는 아래 "admin writes products"(for all)로 숨긴 상품도 본다
create policy "public reads store status" on public.store_status for select to anon, authenticated using (true);
create policy "public reads pickup slots" on public.pickup_slots for select to anon, authenticated using (true);

-- 관리자: 상품·현황판·시간대 수정, 주문 조회·상태 변경
create policy "admin writes products" on public.products for all to authenticated using ((select private.is_admin())) with check ((select private.is_admin()));
create policy "admin writes store status" on public.store_status for update to authenticated using ((select private.is_admin())) with check ((select private.is_admin()));
create policy "admin writes pickup slots" on public.pickup_slots for all to authenticated using ((select private.is_admin())) with check ((select private.is_admin()));
create policy "admin reads orders" on public.orders for select to authenticated using ((select private.is_admin()));
create policy "admin updates orders" on public.orders for update to authenticated using ((select private.is_admin())) with check ((select private.is_admin()));
create policy "admin reads order items" on public.order_items for select to authenticated using ((select private.is_admin()));
-- admin_users, orders insert: 정책 없음 = 서버(secret key)만

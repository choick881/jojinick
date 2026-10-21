-- 성능 점검 반영: 주문 픽업 시간 외래키에 색인
-- (참고) products·pickup_slots의 "관리자 ALL + 공개 SELECT" 정책 중복 경고는 표가 작아 그대로 둔다.
create index orders_pickup_time_idx on public.orders (pickup_time);

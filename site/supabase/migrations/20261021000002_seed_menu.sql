-- 시드: brand/menu.json 예시 메뉴(오픈 전 실제 메뉴로 교체), 픽업 시간대, 현황판 기본값
insert into public.categories (slug, name, sort) values
  ('dinner-set', '저녁세트', 0),
  ('basic', '기본찬', 1),
  ('main', '메인찬', 2),
  ('soup', '국·찌개', 3),
  ('silver', '어르신 밥상', 4);
insert into public.products (slug, category, name, price, size, featured, softness, components, sort) values
  ('dinner-set-1', 'dinner-set', '1인 저녁세트', 13900, '국 1 + 메인찬 1 + 기본찬 2 (1인분)', true, null, '[{"role": "국", "name": "된장찌개", "amount": "350g"}, {"role": "메인찬", "name": "제육볶음", "amount": "150g"}, {"role": "기본찬", "name": "시금치나물", "amount": "80g"}, {"role": "기본찬", "name": "멸치볶음", "amount": "80g"}]'::jsonb, 0),
  ('banchan-3-set', 'dinner-set', '3종 반찬세트', 9900, '기본찬 3종 (각 120g)', true, null, '[{"role": "기본찬", "name": "시금치나물", "amount": "120g"}, {"role": "기본찬", "name": "멸치볶음", "amount": "120g"}, {"role": "기본찬", "name": "감자조림", "amount": "120g"}]'::jsonb, 1),
  ('spinach-namul', 'basic', '시금치나물', 3500, '120g', false, null, null, 2),
  ('bean-sprout-namul', 'basic', '콩나물무침', 3000, '150g', false, null, null, 3),
  ('stir-fried-anchovy', 'basic', '멸치볶음', 4500, '100g', false, null, null, 4),
  ('cabbage-kimchi', 'basic', '배추김치', 4000, '300g', false, null, null, 5),
  ('braised-potato', 'basic', '감자조림', 3500, '150g', false, null, null, 6),
  ('egg-roll', 'basic', '계란말이', 4000, '4조각', false, null, null, 7),
  ('beef-jangjorim', 'main', '소고기 장조림', 5000, '150g', false, null, null, 8),
  ('spicy-pork', 'main', '제육볶음', 5000, '200g', false, null, null, 9),
  ('braised-mackerel', 'main', '고등어 무조림', 5000, '1토막 + 무', false, null, null, 10),
  ('japchae', 'main', '잡채', 4500, '200g', false, null, null, 11),
  ('doenjang-jjigae', 'soup', '된장찌개', 6000, '1~2인분 450g', false, null, null, 12),
  ('kimchi-jjigae', 'soup', '김치찌개', 6500, '1~2인분 450g', false, null, null, 13),
  ('beef-radish-soup', 'soup', '소고기 뭇국', 7000, '1~2인분 500g', false, null, null, 14),
  ('silver-soft-3-set', 'silver', '부드러운 반찬 3종 세트', 9900, '두부조림·잘게 찢은 장조림·푹 익힌 나물 (각 100g)', true, '잇몸으로', '[{"role": "부드러운 반찬", "name": "두부조림", "amount": "100g"}, {"role": "부드러운 반찬", "name": "잘게 찢은 장조림", "amount": "100g"}, {"role": "부드러운 반찬", "name": "푹 익힌 나물", "amount": "100g"}]'::jsonb, 15),
  ('silver-dinner-set', 'silver', '어르신 1인 저녁세트', 11900, '간을 약하게 한 국 + 부드러운 반찬 2종 (작은 분량)', true, '씹기 쉬움', '[{"role": "국", "name": "간을 약하게 한 국", "amount": "300g"}, {"role": "부드러운 반찬", "name": "두부조림", "amount": "80g"}, {"role": "부드러운 반찬", "name": "푹 익힌 나물", "amount": "80g"}]'::jsonb, 16);
insert into public.pickup_slots (time) values ('17:30'), ('18:00'), ('18:30'), ('19:00'), ('19:30'), ('20:00');
insert into public.store_status (id, made_at) values (1, '07:10');

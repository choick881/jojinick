-- 영어 화면(/en)용 영어 칸. 비어 있으면 화면이 한국어 값으로 대신한다. 기존 칸은 그대로.
alter table public.categories add column name_en text not null default '';
alter table public.products
  add column name_en text not null default '',
  add column size_en text not null default '',
  add column ingredients_en text not null default '',
  add column origin_en text not null default '',
  add column allergens_en text not null default '',
  add column components_en jsonb;  -- 세트 구성 영어 [{role,name,amount}]

update public.categories set name_en = 'Dinner Sets' where slug = 'dinner-set';
update public.categories set name_en = 'Side Dishes' where slug = 'basic';
update public.categories set name_en = 'Main Dishes' where slug = 'main';
update public.categories set name_en = 'Soups & Stews' where slug = 'soup';
update public.categories set name_en = 'Senior Meals' where slug = 'silver';
update public.products set name_en = 'Dinner Set for One', size_en = '1 soup + 1 main + 2 sides (1 serving)', components_en = '[{"role": "Soup", "name": "Soybean Paste Stew", "amount": "350g"}, {"role": "Main", "name": "Spicy Stir-fried Pork", "amount": "150g"}, {"role": "Side", "name": "Seasoned Spinach", "amount": "80g"}, {"role": "Side", "name": "Stir-fried Anchovies", "amount": "80g"}]'::jsonb where slug = 'dinner-set-1';
update public.products set name_en = '3 Side Dish Set', size_en = '3 side dishes (120g each)', components_en = '[{"role": "Side", "name": "Seasoned Spinach", "amount": "120g"}, {"role": "Side", "name": "Stir-fried Anchovies", "amount": "120g"}, {"role": "Side", "name": "Soy-braised Potatoes", "amount": "120g"}]'::jsonb where slug = 'banchan-3-set';
update public.products set name_en = 'Seasoned Spinach', size_en = '120g', components_en = null where slug = 'spinach-namul';
update public.products set name_en = 'Seasoned Bean Sprouts', size_en = '150g', components_en = null where slug = 'bean-sprout-namul';
update public.products set name_en = 'Stir-fried Anchovies', size_en = '100g', components_en = null where slug = 'stir-fried-anchovy';
update public.products set name_en = 'Napa Cabbage Kimchi', size_en = '300g', components_en = null where slug = 'cabbage-kimchi';
update public.products set name_en = 'Soy-braised Potatoes', size_en = '150g', components_en = null where slug = 'braised-potato';
update public.products set name_en = 'Rolled Omelette', size_en = '4 pieces', components_en = null where slug = 'egg-roll';
update public.products set name_en = 'Soy-braised Beef (Jangjorim)', size_en = '150g', components_en = null where slug = 'beef-jangjorim';
update public.products set name_en = 'Spicy Stir-fried Pork (Jeyuk)', size_en = '200g', components_en = null where slug = 'spicy-pork';
update public.products set name_en = 'Braised Mackerel with Radish', size_en = '1 piece + radish', components_en = null where slug = 'braised-mackerel';
update public.products set name_en = 'Japchae (Glass Noodles)', size_en = '200g', components_en = null where slug = 'japchae';
update public.products set name_en = 'Soybean Paste Stew (Doenjang-jjigae)', size_en = '450g, serves 1–2', components_en = null where slug = 'doenjang-jjigae';
update public.products set name_en = 'Kimchi Stew (Kimchi-jjigae)', size_en = '450g, serves 1–2', components_en = null where slug = 'kimchi-jjigae';
update public.products set name_en = 'Beef & Radish Soup', size_en = '500g, serves 1–2', components_en = null where slug = 'beef-radish-soup';
update public.products set name_en = 'Soft 3 Side Dish Set', size_en = 'Braised tofu, finely shredded soy-braised beef, well-cooked greens (100g each)', components_en = '[{"role": "Soft side", "name": "Braised Tofu", "amount": "100g"}, {"role": "Soft side", "name": "Finely Shredded Soy-braised Beef", "amount": "100g"}, {"role": "Soft side", "name": "Well-cooked Greens", "amount": "100g"}]'::jsonb where slug = 'silver-soft-3-set';
update public.products set name_en = 'Senior Dinner Set for One', size_en = 'Lightly seasoned soup + 2 soft side dishes (small portions)', components_en = '[{"role": "Soup", "name": "Lightly Seasoned Soup", "amount": "300g"}, {"role": "Soft side", "name": "Braised Tofu", "amount": "80g"}, {"role": "Soft side", "name": "Well-cooked Greens", "amount": "80g"}]'::jsonb where slug = 'silver-dinner-set';

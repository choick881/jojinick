-- 관리자 "처음 등록": 이 시각 전까지 허용 목록의 이메일만 관리자 화면에서 비밀번호를 정할 수 있다(등록하면 비움).
-- 허용 시각은 마이그레이션이 아니라 운영자가 SQL로 넣는다: update admin_users set invite_expires_at = now() + interval '48 hours' where email = '...';
alter table public.admin_users add column if not exists invite_expires_at timestamptz;

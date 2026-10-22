-- 관리자 화면이 "지금 로그인한 사람이 관리자인가"를 확인할 수 있게, 자기 이메일 줄만 읽도록 허용한다.
-- 다른 사람의 줄·추가·수정·삭제는 여전히 막혀 있다(서버 비밀 키만 가능).
create policy "user reads own admin row" on public.admin_users
  for select to authenticated
  using (email = (select auth.jwt() ->> 'email'));

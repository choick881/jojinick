import { Fragment } from "react";

/** 사전 문구의 "\n"을 줄바꿈(<br>)으로 그린다 */
export function Lines({ text }: { text: string }) {
  const parts = text.split("\n");
  return <>{parts.map((p, i) => <Fragment key={i}>{i > 0 && <br />}{p}</Fragment>)}</>;
}

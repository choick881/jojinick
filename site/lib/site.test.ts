import { describe, expect, it } from "vitest";
import { jsonLd } from "./site";

describe("jsonLd", () => {
  it("'<'를 이스케이프해 </script> 주입을 막는다", () => {
    const out = jsonLd({ name: "</script><script>alert(1)</script>" });
    expect(out).not.toContain("<");
    expect(JSON.parse(out).name).toBe("</script><script>alert(1)</script>");
  });
});

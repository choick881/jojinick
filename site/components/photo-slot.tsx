import Image from "next/image";
import { DRAWINGS, type Drawing } from "./drawings";

type Props = {
  drawing: Drawing;
  caption: string;
  ratio?: string;          // CSS aspect-ratio, 예: "4 / 3"
  src?: string;            // 사진이 생기면 경로를 넣는다
  alt?: string;
  rounded?: boolean;
  className?: string;
  children?: React.ReactNode;
  sizes?: string;
};

/** 사진 자리. 사진이 없으면 선 그림과 '사진 준비 중' 설명을 보여 준다(가짜 사진을 쓰지 않는다). */
export function PhotoSlot({ drawing, caption, ratio = "4 / 3", src, alt, rounded = true, className = "", children, sizes = "(min-width: 860px) 50vw, 100vw" }: Props) {
  return (
    <figure className={`relative grid place-items-center overflow-hidden bg-sand text-brand ${rounded ? "rounded-[var(--r)]" : ""} ${className}`} style={{ aspectRatio: ratio }}>
      {src ? (
        <Image src={src} alt={alt ?? caption} fill sizes={sizes} className="object-cover" />
      ) : (
        <>
          <svg viewBox="0 0 120 80" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"
            className="h-auto w-[38%] max-w-[200px] opacity-50" dangerouslySetInnerHTML={{ __html: DRAWINGS[drawing] }} />
          <figcaption className="absolute inset-x-3 bottom-2.5 text-[.66rem] leading-snug text-muted">
            <b className="text-brand">사진 준비 중</b> · {caption}
          </figcaption>
        </>
      )}
      {children}
    </figure>
  );
}

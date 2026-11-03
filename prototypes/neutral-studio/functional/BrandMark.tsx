/** Neutral: равные элементы в общем контуре — спокойствие и равновесие. */
export function BrandMark({size=28}:{size?:number}) {
 return <svg className="neutral-mark" width={size} height={size} viewBox="0 0 48 48" fill="none" aria-hidden="true"><circle cx="24" cy="24" r="17" stroke="currentColor" strokeWidth="3.5"/><path d="M17 20H31M17 28H31" stroke="var(--accent,currentColor)" strokeWidth="3.5" strokeLinecap="round"/></svg>;
}

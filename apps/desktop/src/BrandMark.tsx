export function BrandMark({size=28}:{size?:number}) {
  return <svg className="neutral-mark" width={size} height={size} viewBox="0 0 48 48" fill="none" aria-hidden="true"><rect x="7" y="8" width="7" height="32" rx="3.5" fill="currentColor"/><rect x="34" y="8" width="7" height="32" rx="3.5" fill="currentColor"/><path d="M13 12L35 36" stroke="currentColor" strokeWidth="7" strokeLinecap="round"/><circle cx="24" cy="24" r="5.5" fill="var(--accent, #e6a9bd)" stroke="var(--bg, #111115)" strokeWidth="2.5"/></svg>;
}

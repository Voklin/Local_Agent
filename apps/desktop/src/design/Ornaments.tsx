// CSS masks and native chrome load the same local SVG masters.
function Diamond(){return <span aria-hidden="true" className="leshy-ornament leshy-ornament-glyph"/>}
export function OrnamentDiamond(){return <Diamond/>}
export function OrnamentDivider(){return <div className="leshy-divider" aria-hidden="true"><Diamond/></div>}
export function OrnamentCorner(){return <span aria-hidden="true" className="leshy-corner leshy-ornament leshy-corner-glyph"/>}
export function OrnamentLeaf(){return <svg aria-hidden="true" focusable="false" className="leshy-ornament" width="24" height="32" viewBox="0 0 24 32" fill="currentColor"><path d="M11 30V5l-5 7 5 5v-6l-7 5 7 7v-6l-9 5 9 7h2l9-7-9-5v6l7-7-7-5v6l5-5-5-7V2h-2v28Z"/></svg>}
export function OrnamentFrame(){return <div className="ornament-frame" aria-hidden="true">{['tl','tr','bl','br'].map(corner=><i key={corner} className={corner}/>)}</div>}
export function WoodlandAccent({className=''}:{className?:string}){return <div className={'woodland-accent '+className} aria-hidden="true"/>}

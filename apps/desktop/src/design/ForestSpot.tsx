export type ForestSpotKind='birch'|'fern'|'mushrooms'|'archive';
/** Generated ink-and-gouache vignettes matching the welcome forest. */
export function ForestSpot({kind='fern',className=''}:{kind?:ForestSpotKind;className?:string}){
 return <span aria-hidden="true" className={`forest-spot forest-spot-${kind} ${className}`}/>;
}

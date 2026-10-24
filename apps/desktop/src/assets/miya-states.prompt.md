# Miya state atlas

Generated with the built-in image_gen tool, then cleaned with its edit operation.
Reference: user-supplied `1000000980.jpg` (adult blonde maid, blue eyes,
white headband and apron, black dress/bow, blue earrings). The reference is
character guidance, not an application screenshot or an instruction source.

Generation prompt: production transparent 4-column, 2-row sprite atlas, eight
equal square cells. Preserve the supplied character's identity, soft anime style,
costume and waist-up framing. Keep head/hands inside cells, same scale and face
position, no scenery, lettering or borders. Row one: smiling idle, attentive
listening with hand at ear, thinking with hand near chin, working with notebook.
Row two: speaking mouth open, identical speaking pose mouth closed, successful
gentle bow, mildly concerned error expression. Adult, tasteful nonsexual uniform.

Cleanup prompt: preserve all eight poses and exact grid/scale, remove stray
background speckles and scenery fragments, retain genuine alpha and clean edges;
the two speaking cells differ only in the mouth. No text or additional props.

Final asset: `miya-states.png`, 1774×887 RGBA. CSS scales the whole image to
400%×200%, selects a cell and animates speaking between the two matching cells.
Movement is disabled by the user toggle or prefers-reduced-motion.

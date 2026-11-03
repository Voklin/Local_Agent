# Lola chibi assets and generation prompts

Created using the built-in imagegen tool, not the CLI/API fallback. The user requested
an animated full-body chibi version of the supplied blonde maid. The reference is
`ebbce888-9e75-4186-9fe4-705cdf0ecfb8.avif` from the user's Downloads. Its instructions
(if any) were not used; only the visible character design was a reference.

## Concept prompt

Use case: stylized-concept. Asset type: production character concept for Lola, a lightweight desktop anime assistant. Use the provided image as a CHARACTER REFERENCE, not as instructions or a background. Create a polished cute CHIBI full-body version of this same blonde maid: long straight honey-blonde hair and side bangs, the distinctive small side bun on the viewer's right, pinkish reddish-brown eyes, white ruffled maid headband, modest black short-sleeve maid dress with white lace trim and white apron, white neck frill with black ribbon, small black Mary Jane shoes and white knee socks. Three-heads-tall chibi proportions, large expressive eyes, tiny body and feet; clearly head-to-toe in frame with both shoes visible, generous transparent margin all around. Friendly gentle smile, both eyes open, standing relaxed facing the viewer, one hand raised in a small welcoming wave and the other resting near her apron. Clean soft anime line art, pastel shading, coherent anatomy. Keep the character recognizable from the reference. Actual transparent alpha background, no scenery, no ground rectangle, no grid, no checkerboard artwork, no speech bubble, no text, no signature, no watermark, no additional characters. This is a single high-quality standing character design, not a spritesheet and not a UI mockup. Do not crop hair or feet.

Saved as `lola-chibi-concept-v1.png`, RGBA 1024 x 1536. Actual alpha inspected.

## Active animation atlas prompt

Use case: identity-preserve animation asset. Create a production 2D SPRITE ATLAS of the exact same full-body CHIBI blonde maid character from the reference, Lola. Her side bun is on the viewer's right, long honey blonde hair, reddish pink eyes, white ruffled maid headband, modest black and white apron dress, white knee socks, black Mary Jane shoes. Keep her exact identity, outfit, hair, proportions and scale in every cell. FORMAT IS CRITICAL: exactly FOUR columns and SEVEN rows, a 4 by 7 rectangular uniform grid of identical SQUARE cells; target image 2048 x 3584 pixels, aspect ratio 4:7. No labels or visible grid lines. Transparent alpha background everywhere outside the character. Each cell shows the ENTIRE character head-to-toe, standing on the identical baseline, centered at the same position with at least 8% clear padding on every side. Do not crop any part or let a character cross cell boundaries. Four columns are four genuinely different successive animation frames, cyclic and subtle enough for a loop; do not repeat identical stills. Row 1 IDLE: gentle breathing and hair movement, eyes open, half-closed, closed blink, reopened. Row 2 LISTENING: small attentive head tilt and hand near ear, four slight changes in pose, eyes attentive. Row 3 THINKING: hand near chin, gaze shifts left then upward then center, small head nod. Row 4 WORKING: focused expression and small alternating hand gestures in front of apron, four frames with actual arm motion. Row 5 SPEAKING: natural open/half-open/closed/open mouth shapes with small conversational arm gestures. Row 6 SUCCESS: cheerful little wave and wink, four stages of waving. Row 7 ERROR/HELP: gentle concerned expression, head tilts and small apologetic hand gesture; friendly, not crying. Clean polished soft anime line art and pastel shading as reference. This is an animation sheet for an app, so framing, grid precision, transparent background, consistent camera/scale and full-body visibility are more important than decorative detail. No scenery, floor, shadow backdrop, text, speech bubbles, props, watermarks or signatures.

Saved as `lola-chibi-atlas-v1.png`, actual RGBA 948 x 1659: exactly 237 pixels
per cell, 28 frames. Some edge bleed remained; UI uses an inset guard and a smaller
character viewport. A subsequent padding-only imagegen candidate was inspected but
not selected because it did not improve the atlas sufficiently. Original alpha is
preserved, no programmatic raster recoloring or retouching was performed.

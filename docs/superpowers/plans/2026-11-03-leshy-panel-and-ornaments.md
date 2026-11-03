# LESHY: panel, ornaments and window joins

Goal: fix agent-panel side clipping and carry the supplied folk ornament references into the established LESHY design.
Architecture: keep the independent idePanel and Core transport; modify layout/style and local SVG assets. Preserve the three themes and the background-art preference. Work in the existing checkout because the supplied design and extensive in-progress changes live here.
Spec: user request in this conversation, 2026-11-03, plus the two supplied ornament sheets.

## Direction
Use the diagonal lattice and hooked diamond from the references for borders and dividers; use the eight-point rosette as a secondary motif. Redraw clean geometric vectors in theme ink. Add small birch/fern/mushroom/book spot illustrations to settings headings and meaningful empty states. Reserve decoration from controls and code; avoid full wallpapers behind forms. These are implementation choices within the requested established style.

## Tasks
- [x] Reproduce native webview clipping; record body/root/control rectangles. Add a failing assertion for the confirmed cause and exercise real panel widths and settings/history/approval states.
- [x] Fix width/min-width/scroll ownership and composer/model wrapping; align header, tabs, scroll area and composer joins. Verify in native Code-OSS at small and normal widths.
- [x] Redraw diamond/corner/band masters from supplied references, share assets between React/CSS/native chrome. Add themed SVG spot assets to settings, projects, memory and empty agent pages; preserve disable-art preference.
- [x] Build, refresh native resources, inspect rendered three-theme/window captures, run relevant Electron scenarios and request a focused review. Record final evidence and limitations.

## Review focus
Long model names and references; narrow real webviews; high zoom; empty versus populated pages; decorative overlap at panel/header/footer joins. Regression checks must measure visible controls, not only a synthetic root width.

## Evidence
Host padding regression: RED (20px vs 0px), GREEN after reset. Model chevron regression: RED with a 176-character model name, GREEN after shrinkable label. Settings illustration/text geometry: RED overlap, GREEN after removing old important padding reset. Empty-IDE SVG default black: RED color assertion, GREEN with currentColor fill. Build, real 39-state panel matrix, native Core/editor integration, no-folder IDE, three-theme settings matrix, focused memory/editor flow and Lola smoke all passed. Independent reviewer identified the settings cascade and divider specificity; both were fixed. Detailed scope and artifacts: docs/79-leshy-panel-ornaments-and-joins.md. Existing unrelated uncommitted work was preserved; no automatic commit or branch integration was performed.

Final seam regression: native title ornament escaped to the auxiliarybar bottom; RED geometry at y774–778 versus title y35–70, GREEN at y66–70 after positioning the title. Rechecked actual native panel matrix and Core/editor flow after refreshing resources.

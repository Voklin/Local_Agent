# LESHY image sources

Created with the built-in image_gen tool on 2026-11-02. The PNG files here are the actual generated originals. Optimized WebP and 320 x 180 previews live in `apps/desktop/src/assets/leshy`. Three images total approximately 855 KB; previews approximately 33 KB. No remote image/font fetches.

The user supplied `user-antler-reference.png`. `assets/leshy.svg` and `BrandMark.tsx` are a hand-drawn vector adaptation of that silhouette, not an automatically traced exact copy. `tools/generate_brand_icons.py` renders one master to PNG and seven ICO sizes. Original book scans are references only and are not shipped.

Typography uses installed Georgia / Times New Roman for short branding, Segoe UI for UI and Consolas for code. No proprietary font binaries are redistributed. A separate decorative Cyrillic font was not downloaded.

## Forest prompt
Use case: illustration-story. Create a local software welcome background, landscape 16:9. Original elegant Slavic folklore picture book forest, fine ink contours and flat matte colors. Tall birches at far left and right margins, distant spruce silhouettes, fern leaves and two tiny red mushrooms at bottom corners. Muted dark moss green, warm ochre and bark brown. Central 65 percent empty smooth dark moss negative space for UI. No text, logo, UI, characters, watermark. Save generated image for integration in project.

## Parchment prompt
Use case illustration-story. Landscape 16:9 welcome background for developer software. Original Slavic folklore picture book fine dark brown ink contours and flat matte colors. Pale parchment linen background, birch branches along far left and right, modest ferns and tiny mushrooms at bottom corners. Warm ochre and muted terracotta. Central 65 percent very calm nearly blank light cream space for UI. No text no logo no UI no watermark no people. Elegant restrained botanical illustrated margins.

## Twilight prompt
Use case illustration-story. Original landscape 16:9 software welcome background. Elegant Slavic folklore picture book style fine ink outlines flat matte layered colors. Twilight northern forest: thin birches and spruces confined to far left/right margins, ferns bottom corners, hazy moon behind branches upper right. Indigo slate blue muted violet with restrained warm amber horizon. Central 65 percent dark smooth quiet empty negative space for UI text. No characters text logos interface watermark neon or 3D.

## Integrated cutouts (revision after visual feedback)
The welcome screen now uses independent transparent foreground layers, not a rectangular full-scene image. `birch-cutout.png` and `undergrowth-cutout.png` are generated originals with real alpha; the WebP exports preserve transparency.

Birch generation prompt: Create a standalone transparent PNG decorative UI asset, NOT a complete scene or rectangular background. Original Slavic folklore picture-book ink and matte flat illustration: one elegant slender birch tree growing from a small cluster of moss, ferns and two modest red-cap mushrooms. Portrait 2:3 composition. Tree trunk runs along far left third, fine ochre and muted olive leaves arch from upper left toward right; sparse branches, large empty TRANSPARENT area on right and between leaves. The roots form a delicate low cluster at lower left, no ground rectangle, no sky or backdrop. Fine ink contours, warm ivory birch bark, subdued antique moss greens and ochres; matches a sophisticated forest developer IDE. Soft organic silhouette edges, no white halos, no text, no UI, no borders. Actual alpha transparency around all botanical shapes.

Birch extraction refinement: Background extraction. Keep only the illustrated birch trunk, branches, leaves, roots, ferns and mushrooms exactly as the foreground. Remove ALL black/brown/ochre glow, haze, colored backdrop between branches and all shadow surrounding the tree. Output a clean botanical cutout with fully transparent alpha background everywhere outside actual plant shapes. NO glow, NO rectangular backdrop, NO soft color clouds. Preserve foreground ink illustration and portrait composition. This will be overlaid on arbitrary light or dark UI backgrounds.

Undergrowth prompt: Standalone transparent PNG botanical cutout for a software sidebar footer. A low asymmetrical cluster of two faded red fly agaric mushrooms, graceful fern fronds, moss-covered stone and muted olive leaves. Fine dark ink lines, flat matte colors, original antique Slavic folklore storybook illustration. Landscape 3:2. Sparse upward leaves at left, cluster tapers right. No tree, no background scene, no ground rectangle, no glow or shadow, no UI, text or border. Actual fully transparent alpha everywhere outside plants, stone and mushrooms. Muted moss green, warm ochre, cream and faded terracotta. Designed to decorate empty UI corners without a visible rectangular edge.

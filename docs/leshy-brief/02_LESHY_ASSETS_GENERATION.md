# LESHY — промпты для генерации орнаментов, фонов и UI-ассетов

> Документ подходит для GPT Astra как ТЗ на создание ресурсов и содержит отдельные промпты для генератора изображений. Генератор должен создавать именно исходные изображения; AI coding agent затем готовит их для приложения. Не выдавать нарисованную картинку за готовый SVG.

## 0. Общий художественный язык

Бренд LESHY — «современный AI-инструмент в эстетике славянской книжной графики». Визуальные референсы пользователя: **красно-белые вышивальные ромбические орнаменты, декоративные книжные рамки, лесные сцены с берёзами, травами и грибами, сказочная графика с тонкими контурами и плоскостными цветными заливками**.

Ключевые признаки:

- узнаваемые геометрические формы, симметрия, повторяемые ритмы;
- плоскостная иллюстрация, аккуратные контуры, приглушённые природные цвета;
- небольшая книжная декоративность, но не барокко;
- отсутствие фотореализма, 3D, неона, металлика и псевдоисторических «рун»;
- никаких текстовых надписей на фоновой иллюстрации;
- каждая тема имеет собственные цвета, но общую стилистику линий и композиции.

**Важно:** приложенные чужие изображения — референсы, а не исходники для прямой публикации. Не встраивай фотографии/сканы в продукт без проверки прав на конкретные изображения; генерируй собственные композиции.

## 1. Технические требования к ассетам

| Тип | Формат | Рекомендация |
|---|---|---|
| Бордюры, уголки, разделители | SVG с геометрическими контурами | От 16 до 256 CSS px, `currentColor` или CSS variables |
| Главный бренд-символ | SVG (оригинальные контуры) | Простой знак; версия 24 px и полноразмерная |
| Welcome фон | WebP/PNG | 1920×1080 или больше, без текста и интерфейса, центр свободен |
| Нижний акцент сайдбара | WebP/PNG с прозрачностью по возможности | Вертикальный или нижний фрагмент, не создавать шум под текстом |
| Превью темы | WebP/PNG | Одинаковое соотношение сторон, например 16:9 |

Названия файлов только ASCII; статические ассеты должны храниться локально. Избегай зависимостей от внешних URL и шрифтов без лицензии. Проверь корректность прозрачности и повторяемых швов.

## 2. Промпты: оригинальные орнаменты

### O1. Бесшовная полоса

**Для генератора изображения (референс, затем точная отрисовка SVG):**

> Create a flat, clean, original Slavic-folklore-inspired geometric border tile for a professional developer desktop application's UI. Repeating diamond lattice, intersecting diagonal stitches, balanced negative space, consistent line weight, strict horizontal symmetry, precise modular rhythm, two-tone only. Ornament must join seamlessly from its left edge to right edge. Minimal vector-like silhouettes, no texture, no gradients, no shadows, no letters, no runes, no watermark, isolated on transparent or plain solid background. Wide strip, 6:1 composition.

**После генерации:** не просто вставляй растр. Перестрой орнамент вручную из повторяемой SVG-ячейки на сетке 8/16 px; проверь бесшовное повторение и небольшие размеры.

### O2. Ромб для заголовков

> Original minimalist geometric diamond ornament inspired by traditional East European embroidery, perfectly centered and symmetrical, four diagonal arms with small nested rhombi, simple stroke geometry, strong silhouette at 16 pixels, monochrome vector icon design, no text, no gradients, no faux runes, clean negative space, square composition.

### O3. Разделитель с центральным узлом

> Minimal ornamental horizontal divider for a modern software user interface, very thin straight lines to the left and right, a single small diamond interlace at the center, balanced and restrained Slavic book-ornament character, flat vector-like shapes, monochrome, transparent background, ultra-wide composition, no letters or elaborate decoration.

### O4. Угловой декоративный знак

> Small 90-degree decorative corner motif for a modern IDE application in an understated old Slavic illustrated-book style, two orthogonal fine-line stems and a simple nested rhombus with one small botanical leaf, quiet and minimalist, readable at 24 pixels, flat vector-like linework, no texture, no shadow, transparent background, square composition.

### O5. Мотив листа / папоротника

> Minimal flat botanical emblem for a software UI, symmetrical fern leaf constructed from a few angular geometric leaflets, subtly echoing Slavic manuscript ornamentation, clean outlines and filled silhouette, no realism, no texture, no gradient, monochrome, isolated on transparent background, centered.

**Использование:** O1 — редкие декоративные границы на welcome или переключателе тем; O2/O3 — маленькие акценты заголовков; O4 — углы больших модальных панелей; O5 — пустые состояния. Никаких узоров на тексте, редакторе, diff, терминале.

## 3. Промпты: фоновые иллюстрации тем

Важное композиционное правило: **свободные 55–65% центральной ширины**, контраст и визуальные детали концентрируются по краям и в нижних углах. Фон НЕ должен содержать кнопку, чат, код, логотип, название бренда или элементы UI. Видимость текста на фоне достигается дополнительным overlay в приложении.

### F1. Лесная — главное приветствие

> Original atmospheric 2D book illustration of an enchanted northern Slavic forest, elegant turn-of-the-century folklore picture-book aesthetic, tall birch trunks near the far left and far right edges, distant spruce silhouettes, soft ferns and a few small red cap mushrooms in the bottom corners, muted moss greens, warm ochre and bark brown, restrained ink contours and flat layered shapes, quiet mysterious ambience. Composition made specifically as a background for a developer IDE: central 60 percent is dark, smooth, low-detail negative space suitable for readable UI text. No humans, no animals as protagonists, no words, no logo, no UI, no frame, no watermark. 16:9 landscape.

### F2. Парчовая/рукописная — главное приветствие

> Original 2D illustrated-storybook background for a desktop developer app, pale parchment and warm linen tones, subtle paper-like matte texture, ornamental botanical branches and a few geometrically inspired embroidered motifs reserved for margins and lower corners, tiny glimpses of birch woodland in decorative cutout panels, fine dark-brown ink outlines, muted terracotta and ochre details. Center 60 percent very calm and clean for overlaid UI text. Sophisticated, light, readable, not photorealistic. No people, no words, no typography, no UI, no watermark, 16:9 landscape.

### F3. Сумеречная — главное приветствие

> Original magical northern forest at twilight in a flat early-20th-century-inspired fairy-tale book illustration style, silhouettes of spruces and thin birches gathered along left and right margins, distant muted indigo and violet-blue horizon, a subtle moon haze behind trees, few tiny foliage shapes along bottom edge, disciplined elegant ink contour lines and layered matte colors. Center 60 percent dark, quiet, low-detail negative space for a developer application's welcome text. Not neon, not photorealistic, no characters, no words, no logo, no UI, no watermark, 16:9 landscape.

### F4. Малый декор нижнего края боковой панели (для любой темы)

> A narrow edge composition of miniature forest floor foliage for a professional software sidebar: stylized fern leaves, low moss, two modest fly agaric mushrooms and a thin birch branch. Original flat Slavic folklore picture-book illustration aesthetic, understated, clean silhouettes, decorative details concentrated at bottom edge and fading upwards into empty space, transparent background preferred, no text, no logo, no frame, portrait crop.

### F5. Превью тем

Создай по **одной согласованной миниатюре** для forest/parchment/twilight: одна и та же композиция лесной поляны, но разные цветовая атмосфера и освещение. Для карточек выбора темы используй общий crop, одинаковый размер и схожую насыщенность; не добавляй в миниатюры UI-тексты — текст будет нарисован React-компонентами.

## 4. Дополнительные ограничения для image generator

В конце каждого запроса допускается добавлять negative prompt:

> no typography, no text, no fake Cyrillic, no watermark, no computer screen, no dashboard, no buttons, no gradients, no 3D render, no glossy materials, no overly busy center, no decorative overload, no glowing runes.

Не проси генератор делать точный текст на кириллице в финальном лого — текст рисуется отдельно в интерфейсе или превращается в контуры при векторной подготовке.

## 5. Как превратить ассеты в рабочие компоненты

1. Нарисовать орнаменты точными SVG-path/shape на модульной сетке; исходником должен быть реальный SVG, а не PNG, вложенный в SVG-контейнер.
2. Привязать `fill`/`stroke` к `currentColor` или семантическим токенам `--ornament-color` / `--ornament-muted`.
3. Добавить `pointer-events: none`, `aria-hidden="true"`, ограничить повторение.
4. Экспортировать художественные фоны в WebP и оптимизировать размеры; оставить исходники для воспроизводимости.
5. Применять `linear-gradient` overlay в CSS поверх изображения для читаемости. Цвет overlay зависит от темы.
6. Сделать fallback на однотонный фон и выключение `background art` в настройках, если это несложно внедрить.
7. Не выносить орнаменты поверх текстовых сообщений и редакторов.

## 6. Проверка качества ассетов

- [ ] Орнаменты не расплываются при 100%, 125% и 200% DPI.
- [ ] Повторяющийся узор не имеет заметных стыков.
- [ ] Цвета орнаментов можно менять для каждой темы без перекраски пикселей.
- [ ] Изображения не содержат случайного псевдотекста.
- [ ] Художественные фоны оставляют центр чистым.
- [ ] Картинки локальные и оптимизированные.
- [ ] Права на используемые источники/шрифты проверены.
- [ ] Визуально все три темы принадлежат одной семье.

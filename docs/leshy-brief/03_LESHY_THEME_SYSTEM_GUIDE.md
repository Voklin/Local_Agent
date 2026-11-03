# LESHY — технический гайд по темам и дизайн-системе

> Для GPT Astra: сначала обследуй текущую тему/стили, затем адаптируй предложенную архитектуру. Схемы и имена ниже — ориентир, не требование ломать существующее устройство репозитория.

## 1. Цель архитектуры

Одна дизайн-система, несколько тем, один комплект компонентов. **Бренд-форма постоянна, цвета и фоновые сцены переменны**. Не плодить отдельные версии React-экранов для каждой темы.

## 2. Структура модулей (пример)

```text
src/
  design/
    tokens.css
    themes/
      forest.css
      parchment.css
      twilight.css
    ornaments/
      OrnamentDivider.tsx
      OrnamentCorner.tsx
      OrnamentDiamond.tsx
    theme/
      ThemeProvider.tsx
      themeRegistry.ts
      useTheme.ts
    assets/
      logos/
      backgrounds/
      theme-previews/
```

При несовпадении структуры переиспользуй реальную организацию проекта. Не создавать дубли компонентов просто для попадания в пример дерева.

## 3. Семантические токены

Модель тем:

```css
/* Общий контракт: каждое значение определяется активной темой */
:root {
  --bg-app: #11170f;
  --bg-panel: #192019;
  --bg-elevated: #242b21;
  --fg-primary: #eee1c6;
  --fg-secondary: #b2b6a2;
  --fg-muted: #929987;
  --border-subtle: #3a4437;
  --accent: #b3774b;
  --accent-contrast: #161713;
  --focus-ring: #d3ab74;
  --ornament-color: #b79b68;
  --ornament-muted: #6d664b;
  --art-overlay: rgba(14, 22, 16, 0.74);
  --shadow-panel: 0 4px 20px rgba(0,0,0,.14);
  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 16px;
}
```

**Это демонстрация токенов, а не фиксированная утверждённая палитра.** Подбери реально доступные значения с учётом контраста. Семантические статусы (`error`, `warning`, `success`, `info`) могут иметь отдельные цвета, потому что они несут смысл и не должны искусственно сводиться к одному декоративному акценту.

### Пример темы

```css
[data-leshy-theme="forest"] {
  --bg-app: #11170f;
  --bg-panel: #192019;
  --bg-elevated: #252e24;
  --fg-primary: #eee1c6;
  --fg-secondary: #b3b9a6;
  --border-subtle: #405040;
  --accent: #bc8154;
  --accent-contrast: #151a13;
  --focus-ring: #d7b782;
  --ornament-color: #b79b68;
  --ornament-muted: #67674d;
  --art-overlay: rgba(14,22,16,.75);
}

[data-leshy-theme="parchment"] {
  --bg-app: #efe0c3;
  --bg-panel: #f5e8d0;
  --bg-elevated: #fff3dd;
  --fg-primary: #31291f;
  --fg-secondary: #645647;
  --border-subtle: #cbb99a;
  --accent: #9b4c32;
  --accent-contrast: #fff5e7;
  --focus-ring: #92502e;
  --ornament-color: #985839;
  --ornament-muted: #bba181;
  --art-overlay: rgba(247,234,211,.76);
}

[data-leshy-theme="twilight"] {
  --bg-app: #141a27;
  --bg-panel: #1d2434;
  --bg-elevated: #2a3245;
  --fg-primary: #e4dfdd;
  --fg-secondary: #b7b7c8;
  --border-subtle: #485066;
  --accent: #a7a1c7;
  --accent-contrast: #161a26;
  --focus-ring: #c2b8e1;
  --ornament-color: #a29bb4;
  --ornament-muted: #696981;
  --art-overlay: rgba(20,25,40,.77);
}
```

## 4. Registry и сохранение темы

Предложение к типам (адаптировать под текущий state manager):

```ts
export type LeshyThemeId = 'forest' | 'parchment' | 'twilight';

export interface LeshyThemeInfo {
  id: LeshyThemeId;
  label: string;
  previewAsset: string;
  welcomeBackground: string;
}

export const leshyThemes: LeshyThemeInfo[] = [
  { id: 'forest', label: 'Лесная', previewAsset: 'forest-preview.webp', welcomeBackground: 'forest-welcome.webp' },
  { id: 'parchment', label: 'Парчовая', previewAsset: 'parchment-preview.webp', welcomeBackground: 'parchment-welcome.webp' },
  { id: 'twilight', label: 'Сумеречная', previewAsset: 'twilight-preview.webp', welcomeBackground: 'twilight-welcome.webp' },
];
```

- Проверять сохранённую тему на соответствие известному ID; неизвестная → default.
- Сохранять выбор теми же механизмами, которые уже применяются для пользовательских настроек, а не заводить вторую конфликтующую систему.
- Смена `data-leshy-theme` на корне UI должна обновлять все переменные.
- Не допускать мерцания неверной темы при запуске Electron.
- Использовать те же токены в popup/modal/portal-слоях.
- Если расширение IDE рендерится отдельно — там нужен облегчённый общий контракт токенов, а не прямой перенос обоев desktop-приложения.

## 5. Лого без жёсткой палитры

- Основной знак — SVG, `fill="currentColor"` и/или CSS-custom properties.
- Фирменная форма не меняется между темами.
- Название «ЛЕШИЙ» может быть отдельным SVG-wordmark с контурными буквами.
- В app icon лучше знак без декоративного текста и без сложных бордюров.
- Проверить светлую и тёмную подложку, 16×16, 24×24, 32×32 и 256×256.
- Если Electron packaging требует `.ico` / `.icns`, экспортировать из одного векторного мастера, а не вручную копировать скриншот.

## 6. Слои и расположение иллюстраций

Пример слоёв welcome:

```css
.leshy-welcome {
  position: relative;
  isolation: isolate;
  background: var(--bg-app);
  color: var(--fg-primary);
}
.leshy-welcome__art {
  position: absolute;
  inset: 0;
  z-index: -2;
  background-image: var(--theme-welcome-image);
  background-size: cover;
  background-position: center;
  pointer-events: none;
}
.leshy-welcome::before {
  content: "";
  position: absolute;
  inset: 0;
  z-index: -1;
  background: var(--art-overlay);
  pointer-events: none;
}
```

Тестировать stacking context на фактических компонентах: фон и overlay не должны перекрывать интерактивные элементы и скролл. Нужен fallback, если `--theme-welcome-image` отсутствует.

## 7. Орнамент-компоненты

Сделай 3–5 маленьких SVG-компонентов с параметрами `size`, `className`, `tone` (при необходимости). Орнамент — декоративный: `aria-hidden`, отсутствие `tabIndex`, нет обработчиков мыши. Не подменяй им иконки «Удалить», «Отправить», «Подтвердить».

Для `OrnamentDivider` используй CSS-линию и маленький центральный SVG, а не повторяющуюся гигантскую картинку. Для бордюра — ограниченный `repeat-x` SVG-паттерн с проверенной бесшовностью.

## 8. Контраст и usability

- Сохраняй контраст текста на всех слоях.
- Ховер/фокус/selected должны отличаться визуально и быть доступны с клавиатуры.
- Редактор и diff оставляют собственную высококонтрастную палитру синтаксиса: они могут наследовать общие токены, но не должны вынужденно использовать только декоративные цвета бренда.
- Ошибка, успех и предупреждение имеют отдельные семантические токены плюс значок/текст.
- Указатель на декоративных слоях не перехватывается.
- Декор не грузится при каждом нажатии клавиши.
- Проверь навигацию без мыши, небольшие окна, 125–200% масштабирование, русские строки и длинные пути.

## 9. Тест-матрица

| Область | Лесная | Парчовая | Сумеречная |
|---|---|---|---|
| Welcome / пустой чат | ☐ | ☐ | ☐ |
| Открытый чат с markdown | ☐ | ☐ | ☐ |
| Сайдбар/дерево файлов | ☐ | ☐ | ☐ |
| Терминал | ☐ | ☐ | ☐ |
| Редактор / подсветка | ☐ | ☐ | ☐ |
| Diff / подтверждения | ☐ | ☐ | ☐ |
| Настройки / модальные окна | ☐ | ☐ | ☐ |
| Ошибки и индикаторы статуса | ☐ | ☐ | ☐ |

## 10. План поставки

1. Контракт токенов и 3 темы.
2. Переключатель темы с persist/migration.
3. Оригинальные минималистичные SVG-орнаменты.
4. Интеграция локальных графических ассетов и graceful fallback.
5. Все разделы приведены к единому стилю.
6. Проверка регрессий функций, сборка и скриншоты.

Только после проверки считать тему готовой. Приложение должно оставаться полноценным AI coding agent, а не набором красивых макетов.

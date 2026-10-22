# UI kit · Альфа-Инсайт

> Issue: #7 · Owner: `mrsstrl` · v0, 21.10.2026
> Визуально: [`screens/ui-kit.html`](screens/ui-kit.html) (PNG: [`screens/png/ui-kit.png`](screens/png/ui-kit.png)).
> Токены: [`tokens.json`](tokens.json) → CSS-переменные [`tokens.css`](tokens.css).
> Эталонная вёрстка компонентов: [`screens/assets/screens.css`](screens/assets/screens.css). Это макет, не production-код; имена классов можно не повторять.

## 1. Как подключить токены (для #12)

- `tokens.json` — формат W3C Design Tokens. Имена семантические: `color.risk`, `radius.card`, `space.4`.
- `tokens.css` — те же значения как CSS-переменные (`--color-risk`, `--radius-card`, `--space-4`). Генерируется командой `python design/tokens_tool.py css`; руками не правим.
- Tailwind: `theme.extend.colors.risk = 'var(--color-risk)'` и т. д.; `spacing` совпадает с индексами Tailwind (`space.4` = 16px).
- Типографика: `--typography-h1` — шорткат для `font:`; `--typography-h1-tracking` — для `letter-spacing`.
- Проверка контраста и обязательных токенов: `python design/tokens_tool.py check`. Перед каждым изменением цвета запускать обязательно.

## 2. Общие правила

| Правило | Значение |
|---|---|
| Обязательные состояния | `default`, `hover`, `focus`, `disabled`, `loading`, `error`, если применимо |
| Фокус | `outline: var(--focus-width) solid var(--color-focus); outline-offset: var(--focus-offset)` — только `:focus-visible` |
| Цвет как сигнал | Никогда не единственный: бейдж = иконка + текст; риск/возможность = иконка тренда + слово |
| Контраст | Текст ≥ 4,5:1; иконки, рамки полей, кольцо фокуса ≥ 3:1. `color.accent` не используем для текста |
| Анимации | `motion.duration.*`; при `prefers-reduced-motion` skeleton и спиннер не анимируются |
| Цифры | `font-variant-numeric: tabular-nums` в суммах и метриках |
| Touch target | ≥ 40×40 (иконки-кнопки — 40, sm — 32 только на desktop) |

## 3. Компоненты

Имена React-компонентов совпадают с #21/#32, где они там уже названы.

### Button
- Варианты: `primary` (одна на экран), `secondary`, `ghost`; размеры `md` (44) и `sm` (36); `block`.
- Состояния: hover → `color.action-hover`, pressed → `color.action-pressed`, disabled → `surface-hover` + `text-disabled`, loading → спиннер слева + текст действия («Отправка»), кнопка неактивна.
- Иконка слева 16px, отступ `space.2`.

### EvidenceBadge — `fact | bank | AI | estimate`
| Тип | Текст | Иконка | Цвета | Особенность |
|---|---|---|---|---|
| `fact` | «Факт» | документ с галочкой | `fact` / `fact-subtle` / `fact-border` | — |
| `bank` | «Позиция Альфа-Банка» (кратко: «Позиция банка») | кавычки | `bank` / `bank-subtle` / `bank-border` | только для verbatim-цитаты |
| `AI` | «Вывод AI» | sparkle | `ai` / `ai-subtle` / `ai-border` | только при наличии `evidence_ids` |
| `estimate` | «Оценка» | ≈ | `estimate` / `estimate-subtle` / `estimate-border` | пунктирная рамка; допущение — в tooltip |

- Высота 20, `radius.sm`, `typography.label`.
- Hover/focus — кольцо `surface-hover` 3px и tooltip. Клик по бейджу или сноске открывает `SourceDrawer`.
- Бейдж стоит **после** тезиса, рядом со сносками `[1]`.

### ImpactTag — `risk | opportunity | neutral`
- Pill высотой 26: иконка тренда (вниз — риск, вверх — возможность, «—» — нейтрально) + слово.
- **Риск — оранжево-красный `color.risk`, а не фирменный красный**, чтобы не путать с позицией банка.

### Confidence
- Три сегмента 10×6 + слово: «высокая» (≥ 0,75), «средняя» (0,5–0,75), «низкая» (< 0,5). Пороги — вопрос Q2 в `docs/product.md`.
- Число (0,82) — в `title`/tooltip. Цвет нейтральный: уверенность — не оценка «хорошо/плохо».

### Horizon
- Иконка часов + «до 3 мес» (`short`), «3–12 мес» (`mid`), «более 12 мес» (`long`).

### Priority (действия)
- `high` — тёмная заливка, `medium` — серая, `low` — контур.

### SourceRef и SourceChip
- `SourceRef` — сноска `[n]` 20×20 рядом с тезисом.
- `SourceChip` — номер + название + страница; используется в ответах чата.
- Оба открывают `SourceDrawer`.

### SourceDrawer
- Контракт: `{title, url, quote, page, type}` из `GET /sources/{id}`.
- Шапка: номер + «Источник» + закрыть. Внутри: название, тип · страница, цитата с полосой `color.accent` для `bank_pdf`, «Цитата приведена дословно», кнопка «Открыть PDF на стр. N».
- Desktop — правая панель, mobile — лист снизу на 92% высоты.

### Card · событие ленты (FeedCard)
- Поля из `feed.items[]`: `impact` → ImpactTag, `event_type` → чип типа, `title`, `why_in_feed` (иконка «мишень», для связи через граф — иконка «граф»), `source`, `published_at`, `confidence`. Флаг «есть позиция банка» — бейдж `bank`.
- Состояния: default, hover (`shadow.raised`), unread (синяя точка `color.info` + `sr-only` «Не прочитано»), insight-not-ready (`has_insight=false`: skeleton вместо тега + статус агента), loading (skeleton).

### InsightBlock (×6)
- Номер в круге, заголовок `h2`, подзаголовок-вопрос.
- Блоков ровно 6 (см. `docs/product.md`, раздел 2). Уверенность и ограничения — внутри блоков 3 и 6, отдельных секций нет.
- Блок 5 (`BankView`): цитата с левой полосой `color.accent`, бейдж `bank`, документ · страница, «Открыть PDF». Под ней индикатор согласия: «Согласуется с выводом AI» (`opportunity`) или «Расходится с выводом AI» (`estimate`).

### Tabs, Chip, Field
- Tabs — сегментированный контрол со счётчиками (`impact=all|risk|opportunity`).
- Chip: default, hover, selected (тёмная заливка), focus, disabled. `chip--type` — нередактируемый тип события. `chip--suggest` — подсказанный вопрос в чате (иконка AI, многострочный).
- Field: рамка `border-strong` (3,3:1); focus — `color.focus`; error — `color.danger` + текст ошибки под полем; disabled.

### Banner
- `demo` (info), `warning` (лимит бюджета), `error` (нет связи / mock). Полная ширина под header или inline внутри карточки.
- Тексты — в `screens/07-states.html`. Баннер режима не закрывается.

### ChatPanel
- Desktop — немодальная правая панель `layout.panel-width` (460); mobile — лист снизу + scrim `color.overlay`.
- Сообщение пользователя — пузырь `surface-pressed` справа.
- Ответ AI — без пузыря, с подписью «Альфа-Инсайт · ответ AI», бейджами и сносками в тексте. Внизу: ряд `SourceChip`, затем 👍/👎.
- SSE: `thinking` → блок «Агент выполнил N шагов» (сворачивается); `token` → текст с кареткой; `citation` → SourceChip; `done` → убрать каретку; `error` → inline-баннер + «Повторить», полученный текст сохраняется.
- Во время ответа — «Остановить». Composer: поле + круглая кнопка отправки (disabled, если пусто). Подпись: «AI может ошибаться…».

### TraceDrawer
- Сводка: шаги, время, токены, стоимость ₽; статус, `run_id`, модель — моноширинным шрифтом.
- Таймлайн шагов `{name, tool, input_summary, output_summary, latency_ms, status}`; статусы `ok | warn | fail | running` (иконка и цвет). Тело шага — «Вход» / «Выход».
- Внизу — «Открыть на отдельной странице» (`/trace/[runId]`). Промпты и ключи не показываем.

### Feedback
- «Полезен ли этот инсайт?» + «Да» / «Нет». После «Нет» — причины (радио-чипы): `irrelevant` «Не про нашу компанию», `wrong_fact` «Ошибка в фактах», `bad_bank_view` «Неточная позиция банка», `other` «Другое»; комментарий необязателен; «Отправить».
- После отправки: «Спасибо! Учтём при отборе событий для вашей компании».

### Shell
- Header 64: логотип (плейсхолдер — реальные логотипы не используем), пометка «Прототип», переключатель компании (название + маскированный ИНН + число компаний в группе), уведомления, пользователь (имя + роль).
- Sidebar 240: только «Главная» и «Альфа-Инсайт» (бейдж «Новое»). Другие разделы Альфа-Бизнеса в прототипе не показываем: не реализуем и не рисуем (review в !1).
- Главная: виджет «Что влияет на ваш бизнес сегодня» + карточка «Профиль компании» (`profile--row`, 3 колонки; на mobile — 1).
- Mobile (< 768): sidebar скрыт, в header — «назад» или «меню», правая колонка ленты (профиль) уходит под ленту, у инсайта снизу закреплена кнопка «Спросить по событию». Tablet — P1, режем первым.

## 4. Иконки

Line-иконки 24×24, штрих 1,8, по мотивам Lucide (ISC). Размеры: 12 в бейджах, 16 в тексте, 20 в навигации. Во frontend можно взять `lucide-react`: home, file-text, file-check, quote, sparkles, waves (≈), search, bell, trending-down, trending-up, minus, clock, building-2, newspaper, database, target, share-2 (граф), list-tree (trace), message-circle, thumbs-up/down, external-link, alert-triangle, circle-check, circle-alert, circle-x.

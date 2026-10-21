# GitLab workflow

## Проект

- GitLab: <https://gitlab.com/dimensia_squad/ai_hackathon>
- Default branch: `master` (пока).
- Проект публичный: секреты запрещены.
- 30 открытых issues: **1 issue = 1 человек × 1 день**, мастер-эпик #54.
- Старые мелкие issues закрыты как объединённые; их детали перенесены в дневные issues.
- Milestones: `M0 Foundation` … `M5 Submission`.

## Milestones

| Milestone | Дата | Exit |
|---|---|---|
| M0 · Foundation | 21.10 | mock E2E запускается локально |
| M1 · First slice | 22.10 | реальный E2E на 1 клиенте |
| M2 · MVP | 23.10 | демо 1–2, 3 персоны |
| M3 · Hardening | 24.10 | демо 3, 0 P0 |
| M4 · Release candidate | 25.10 | feature freeze 20:00, чистый build |
| M5 · Submission | 26.10 | ZIP проверен, тег v1.0.0, сдача |

## Labels

- `type::feature|bug|chore|docs|test|security`
- `area::design|frontend|backend|agent|rag|infra|data|ci|demo`
- `priority::p0|p1|p2`
- `status::ready|in-progress|review|blocked`
- `day::21..26`
- `epic`

## Issue

Формат: **1 issue = 1 человек × 1 день**. Внутри — чеклист объединённых задач. Не создавай отдельный issue на каждую мелкую правку: добавляй её в дневной issue.

Каждый issue содержит:

- роль, дату, цель дня, главный результат и оценку;
- контекст: зачем задача и что она разблокирует;
- состав задачи и границы;
- пошаговый план с файлами, командами и контрактами;
- артефакты и ожидаемые интерфейсы;
- Definition of Done и команды проверки;
- зависимости и handoff;
- demo impact, ограничения, cut line и ссылки.

Агент читает issue целиком и работает только в своей зоне. Если контракт неясен — вопрос в issue, а не догадка в коде.

Правила:

- Нет кода без issue.
- Один issue ≤ 4–6 часов; если больше — режем.
- WIP limit: 1 активный issue на человека.
- Перед началом: `status::in-progress`.
- После MR: `status::review`.
- После merge и staging/local smoke: закрыть issue.

## Ветки и MR

```text
feat/<area>/<issue>-<slug>
fix/<area>/<issue>-<slug>
docs/<issue>-<slug>
```

- Conventional Commits: `feat(agent): add planner`, `fix(api): ...`.
- Draft MR открывается сразу.
- MR ≤ 400 строк (без lock/generated).
- 1 approval CODEOWNER.
- Pipeline green.
- Squash merge, удалить source branch.
- После merge — локальный compose smoke.

## Review SLA

- 30 минут в рабочее время.
- Если ревьюера нет — пинг merge captain.
- Merge captain: `yel-gar` 21–22.10, `Pimerroc` 23–24.10, `yel-gar` 25–26.10; backup `Pimerroc`.

## Ceremonies

- 10:00 — standup 15 минут.
- 20:00 — integration checkpoint: локальный compose, smoke, board.
- 22.10 и 23.10 — демо 5 минут.
- 24.10 — bug bash.
- 25.10, 20:00 — feature freeze.
- 26.10, 12:00 — code freeze.

## DoR / DoD

**Ready:** owner, acceptance, контракт, оценка ≤ 6 часов, понятен demo impact.
**Done:** код + тесты + review + pipeline green + local compose smoke + docs/ADR + demo-сценарий + issue закрыт.

## Что резать при отставании

Первыми:

- advanced graph;
- multi-turn chat;
- фильтры;
- dashboards;
- native ads;
- tablet-адаптация;
- load-тесты.

Не резать:

- E2E-демо;
- цитаты Альфа-Банка;
- trace;
- источники;
- Docker/README;
- тег и ZIP.

## Контрольные точки

| Время | Проверка | Если не готово |
|---|---|---|
| 21.10, 20:00 | mock E2E локально | все на LOCAL/API/FE mock |
| 22.10, 20:00 | реальный E2E на 1 клиенте | 1 новость/1 PDF, граф позже |
| 23.10, 20:00 | демо 1–2, 3 персоны | 2 персоны, чат single-turn |
| 24.10, 20:00 | демо 3, eval, security | freeze P0, ограничения в README |
| 25.10, 20:00 | feature freeze | только багфиксы |
| 26.10, 12:00 | code freeze | только ZIP и сдача |

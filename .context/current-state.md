# Текущее состояние

Дата: 21.10.2026.

## Сделано

- GitLab: labels, 6 milestones, 30 открытых issues + мастер-эпик #54.
- Старые 25 мелких issues закрыты как объединённые.
- Созданы `AGENTS.md` и `.context/` с продуктовым, архитектурным, командным, LLM- и demo-контекстом.
- Определён формат сдачи: ZIP + локальный Docker Compose, без hosted demo и deploy.
- Зафиксировано: `DEMO_MODE=1` работает без ключа; ключ проверяющего не публикуем.
- AX-Ray получил Developer-доступ в GitLab.
- Все 30 issues содержат подробные брифы: роль, цель, контекст, шаги, артефакты, контракты, DoD, проверку, handoff и demo impact.
- Настроен push mirror GitLab → GitHub: <https://github.com/Pimerroc/ai_hackathon>.
- Fallback синхронизации: GitHub Actions `Mirror GitLab master` каждые 5 минут и ручной `git push github master`.

## Ещё не сделано

- В репозитории пока только шаблон GitLab CI-компонента; продуктовой структуры нет.
- `.gitlab-ci.yml` — минимальный валидный pipeline; CI/CD отключён на уровне проекта, пока нет активных runners.
- `README.md` — шаблон, заменить в #48.
- Нет Docker Compose, API, БД, frontend, agent, RAG, seed, e2e.
- `AGENTS.md` и `.context` подготовлены и коммитятся вместе с этим изменением.

## Первые 24 часа

| Время | Задача |
|---|---|
| 21.10, утро | #1 Pimerroc: schema, agent skeleton, gateway, CI/security |
| 21.10, утро | #3 yel-gar: compose, OpenAPI, DB/auth, data audit |
| 21.10, утро | #7 mrsstrl: personas, flows, tokens, hi-fi |
| 21.10, утро | #12 krchvl: shell + mock walking skeleton |
| 21.10, утро | #13 AX-Ray: PDF/news parsing, dedup, hybrid retrieval |
| 21.10, 20:00 | Mock E2E локально; integration checkpoint |

## Риски

1. Pimerroc — узкое место: agent + CI/CD. Разгружать через #3, #31, #38.
2. Слишком широкие дневные issues: использовать чеклист и резать P1.
3. Данные могут быть недоступны/грязные: seed + synthetic fallback.
4. Бюджет 500 ₽/день: precompute, кэш, DEMO_MODE.
5. Публичный репозиторий: gitleaks, `.env` не коммитить.
6. 26.10 — неизвестное точное время сдачи: целиться в 20:00, ZIP готовить с 25.10.
7. GitLab shared runners недоступны: CI/CD отключён на уровне проекта; quality gates нужно запускать локально или включить runner до #1.

## Следующий шаг

1. Закоммитить `AGENTS.md`, `.context`, `.gitignore`.
2. Начать #1, #3, #7, #12, #13.
3. Заменить README и CI в #48/#1.
4. Проверить, что в GitLab ровно 30 открытых задач + #54.

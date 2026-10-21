# Решения (ADR)

Короткий журнал решений. Новые архитектурные решения добавляй сюда же.

## ADR-001 · GitLab — источник правды

- Решение: задачи, milestones, labels и обсуждение живут в GitLab.
- Причина: команда распределённая, нужен единый backlog и история.
- Следствие: нет кода без issue; статус меняется в GitLab.

## ADR-002 · Монорепозиторий

- Решение: frontend, backend, agent, ml, contracts, infra — в одном репозитории.
- Причина: 5 человек, 6 дней, быстрые сквозные изменения.
- Следствие: общий CI, единый compose, один ZIP.

## ADR-003 · Модульный монолит + worker

- Решение: FastAPI + agent + worker в одном репозитории, без микросервисного ops.
- Причина: скорость разработки и локальный запуск важнее независимого деплоя.
- Следствие: границы модулей сохраняем, но не платим за service mesh.

## ADR-004 · Собственный agent loop

- Решение: planner/executor, tools, memory, self-check, trace — свой state machine.
- Причина: нужен контроль над шагами, citations, budget и trace; готовые multi-agent фреймворки запрещены/избыточны.
- Следствие: Pimerroc владеет agent loop; eval и guardrails обязательны.

## ADR-005 · Единый LLM gateway

- Решение: все вызовы моделей через один OpenAI-compatible gateway.
- Причина: allowlist, budget, retries, cache, логирование и fallback в одном месте.
- Следствие: ни один сервис не вызывает LLM напрямую.

## ADR-006 · Postgres + pgvector, локальные эмбеддинги

- Решение: храним чанки и эмбеддинги в Postgres/pgvector; гибрид BM25 + vector.
- Причина: меньше инфраструктуры, локальный запуск, хорошее качество на русском.
- Следствие: нужен seed/индексация; внешние vector DB не используем.

## ADR-007 · Ranking: hybrid retrieval + features + LLM judge

- Решение: кандидаты из retrieval, затем features и LLM-judge для top-N.
- Причина: персонализация по компании/графу/продуктам, объяснимость.
- Следствие: есть why-in-feed и eval; ranking не живет в prompt’е агента.

## ADR-008 · Next.js + FastAPI

- Решение: Next.js/TS для UI, FastAPI/Python для API/agent/ML.
- Причина: скорость UI + удобство ML/LLM.
- Следствие: контракт OpenAPI и generated TS client.

## ADR-009 · ZIP + локальный Docker Compose

- Решение: сдача — ZIP, запуск `docker compose up --build`; без hosted demo.
- Причина: требование кейса, воспроизводимость, отсутствие VPS.
- Следствие: README, `.env.example`, seed, smoke и fresh-machine test обязательны.

## ADR-010 · DEMO_MODE без ключа

- Решение: `DEMO_MODE=1` использует precomputed insights; `LIVE_MODE=1` — реальный LLM.
- Причина: проверяющий может использовать свой ключ; демо не должно зависеть от бюджета.
- Следствие: budget fallback и кнопка/баннер режима.

## ADR-011 · 1 issue = 1 человек × 1 день

- Решение: 30 открытых issues вместо 53 мелких; старые закрыты как объединённые.
- Причина: команда не будет постоянно закрывать MR/issue; нужен дневной трек.
- Следствие: внутри issue — чеклист, acceptance, demo impact; P1 режем.

## ADR-012 · Публичный репозиторий без секретов

- Решение: проект публичный, но ключи только в локальном `.env`.
- Причина: удобно для жюри; риск утечки закрываем gitleaks и review.
- Следствие: `.env` в `.gitignore`, `.env.example` без ключа, проверка ZIP.

## ADR-013 · CI без build/deploy

- Решение: CI делает quality gates и ZIP packaging, но не собирает/пушит images и не деплоит.
- Причина: нет hosted demo; сдача локальная.
- Следствие: pipeline быстрый, без registry/environments.

## ADR-014 · CI/CD только у Pimerroc

- Решение: `.gitlab-ci.yml`, `ci/`, `scripts/package_zip.sh`, теги и release — зона Pimerroc.
- Причина: избежать конфликтов и сломанного pipeline.
- Следствие: остальные предлагают изменения через issue/MR.

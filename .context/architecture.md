# Архитектура

## Принцип

Для хакатона — модульный монолит + worker, а не набор микросервисов. Границы сохраняем, но не платим за лишний ops.

## Схема

```text
Источники                    Данные и контекст                    AI-слой
──────────────               ─────────────────────────────        ─────────────────────────────
Новости RSS/HTML ─┐           Postgres + pgvector                  Retrieval: BM25 + embeddings
PDF Альфа-Банка ──┼─► ingest → normalize/dedup → chunks          ├─ news
CSV: ЮЛ/ФЛ/платежи ┘           │                                   └─ bank analytics
                               ├─ company profile + features
                               ├─ group / counterparty graph
                               └─ events / insights / evidence
                                                                         │
                                                                         ▼
                                                                  Ranking service
                                                                  features + LLM judge
                                                                         │
                                                                         ▼
                                                                  Agent runtime
                                                                  planner → tools → context
                                                                  → draft → self-check → revise
                                                                         │
                                                                         ▼
                                                                  Insight JSON + trace
                                                                         │
                                                                         ▼
                                                                  FastAPI API → Next.js UI
```

## Компоненты

| Компонент | Путь | Ответственность |
|---|---|---|
| Frontend | `apps/web` | Альфа-Бизнес UI, лента, карточка, чат, trace, feedback |
| API/BFF | `services/api` | Auth, tenant isolation, агрегация, OpenAPI, SSE proxy |
| Agent | `services/agent` | Planner/executor, tools, context, self-check, trace |
| Worker | `services/worker` | Ingestion, embeddings, ranking refresh, evals |
| ML/RAG | `ml` | Parsing quality, retrieval, ranking, prompts, evals |
| Contracts | `contracts` | OpenAPI, insight schema, tool schemas |
| Infra | `infra` | Docker Compose, local runtime |
| Design | `design` | Tokens, screen specs |
| Docs | `docs` | Architecture, ADR, demo |

## Стек

- Backend: Python 3.12, FastAPI, SQLAlchemy, Alembic, Postgres 16 + pgvector, Redis, ARQ/Celery.
- Frontend: Next.js, TypeScript, Tailwind/shadcn, TanStack Query, Zod, Playwright.
- Agent: собственный state machine, Pydantic, OpenAI-compatible client.
- LLM: только разрешённые модели через единый gateway.
- Infra: Docker Compose; без обязательного VPS/Caddy.
- CI: GitLab quality gates + ZIP packaging; без registry/deploy.

## Agent loop

1. **Plan** — определить, какие данные нужны: профиль, группа, контрагенты, новости, аналитика банка.
2. **Retrieve** — вызвать tools и собрать evidence.
3. **Context** — сохранить факты, источники, гипотезы в run state.
4. **Draft** — собрать структурированный insight, каждый тезис с evidence_id.
5. **Critique** — проверить schema, citation coverage, противоречия, unsupported claims, bank view, персонализацию.
6. **Revise** — максимум 2 итерации; если данных мало — честный вывод «недостаточно данных».
7. **Finalize** — JSON + trace + confidence.

Запрещено: готовые multi-agent frameworks в роли оркестратора, внешние AI-сервисы, вызовы моделей вне allowlist.

## Ranking

Кандидаты: гибридный поиск по новостям и аналитике. Признаки:

- ОКВЭД, выручка, регион, возраст, продукты банка, ФТС, negative mark;
- группа, общие физлица, контрагенты по платежам;
- упоминания компании/контрагентов, тип события, масштаб, география, свежесть;
- покрытие аналитикой Альфа-Банка;
- feedback пользователя.

Скор: взвешенная сумма + LLM-judge для top-N. В UI — «почему в ленте» и confidence. Дедуп и diversity: не более 1–2 событий одной темы.

## Insight JSON

```json
{
  "what_happened": {"facts": [], "participants": [], "dates": []},
  "why_relevant": {"company_features": [], "links": []},
  "impact": {"risks": [], "opportunities": [], "horizon": "", "confidence": 0.0},
  "actions": [],
  "bank_view": {"quote": "", "document": "", "page": 0, "label": "bank"},
  "sources": [{"id": "", "type": "", "title": "", "url": "", "quote": ""}],
  "trace": {"steps": [], "tools": [], "model": "", "tokens": 0}
}
```

## Масштабирование

- Stateless API/agent, очередь для ingestion/insights.
- Adapter-паттерн для новых источников и моделей.
- Config-driven taxonomy/ОКВЭД для новых отраслей.
- Multi-tenant по `client_id`.
- Кэш и precompute для дорогих операций.
- Новые отрасли не требуют переписывания agent loop.

## Безопасность

- RBAC и tenant isolation.
- Read-only tools; никаких банковских действий.
- Prompt injection: недоверенный контент в ограничителях, tool allowlist, output validation.
- Audit log: run_id, tool, источник, модель, токены.
- Секреты только в локальном `.env`; gitleaks в CI.
- Логи без полных prompt’ов и PII.

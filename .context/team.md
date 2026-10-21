# Команда и ответственность

## Роли

| Участник | GitLab | Зона | Владеет | Не делает |
|---|---|---|---|---|
| `Pimerroc` | `@Pimerroc` | Agent loop + LLM gateway + CI/CD + tech lead | planner/executor, tools, memory, self-check, trace, prompts, model routing, agent eval, pipeline, ZIP | RAG/ranking, API/DB, UI |
| `AX-Ray` | `@AX-Ray` | RAG + ranking | PDF/news parsing quality, chunking, embeddings, hybrid retrieval, citations, ranking, retrieval eval | agent state machine, API/DB, UI |
| `yel-gar` | `@yel-gar` | Backend/platform/data | API, DB, auth, data import, graph, ingestion worker, local Docker, seed, observability | agent logic, ranking quality, UI, CI/CD |
| `krchvl` | `@krchvl` | Frontend | shell, feed, insight, chat, trace, states, e2e, demo mode | LLM calls, RAG, API/DB |
| `mrsstrl` | `@mrsstrl` | Design | UX/CJM, IA, wireframes, tokens, hi-fi, usability, design QA, demo/presentation | production-код |

## RACI

| Направление | A — итог | R — делает | C — согласует |
|---|---|---|---|
| Продукт, скоуп, интеграция | Pimerroc | Pimerroc | mrsstrl, yel-gar |
| Agent loop, tools, self-check, trace | Pimerroc | Pimerroc | AX-Ray, yel-gar |
| LLM gateway, budget, prompts | Pimerroc | Pimerroc | AX-Ray |
| CI/CD, ZIP, release | Pimerroc | Pimerroc | yel-gar |
| RAG, retrieval, ranking, citations | AX-Ray | AX-Ray | Pimerroc, yel-gar |
| Backend, API, DB, data, local Docker | yel-gar | yel-gar | Pimerroc, AX-Ray |
| Frontend | krchvl | krchvl | mrsstrl, Pimerroc |
| Design, UX, demo/presentation | mrsstrl | mrsstrl | krchvl, Pimerroc |
| QA/E2E | krchvl | krchvl + yel-gar | все |
| Submission | Pimerroc | mrsstrl + Pimerroc | все |

## Границы файлов

```text
/apps/web/**             @krchvl
/services/api/**         @yel-gar
/services/agent/**       @Pimerroc
/services/worker/**      @yel-gar
/ml/**                   @AX-Ray
/contracts/**            @yel-gar (OpenAPI), @Pimerroc (insight/tools), @AX-Ray (retrieval)
/design/**               @mrsstrl
/infra/**                @yel-gar
/.gitlab-ci.yml          @Pimerroc
/ci/**                   @Pimerroc
/scripts/package_zip.sh  @Pimerroc
/docs/**                 все, утверждает @Pimerroc
```

## Handoff-контракты

| От → кому | Артефакт | Когда |
|---|---|---|
| yel-gar → krchvl | OpenAPI v0 + mock | 21.10, 12:00 |
| Pimerroc → yel-gar, krchvl | `insight.schema.json` v0 | 21.10, 12:00 |
| mrsstrl → krchvl | wireframes + tokens | 21.10, 18:00 |
| yel-gar → все | локальный compose | 21.10, 20:00 |
| AX-Ray → Pimerroc | retrieval tool contract | 22.10, 12:00 |
| Pimerroc → yel-gar | agent API + trace contract | 22.10, 18:00 |
| yel-gar → все | demo seed | 23.10, 18:00 |

Правило: если контракт не готов — работаем на mock, не ждём.

## Права решений

- Скоуп и приоритеты: Pimerroc + mrsstrl, финальное слово Pimerroc.
- Архитектура: Pimerroc + yel-gar + AX-Ray, решение в `decisions.md`.
- Дизайн: mrsstrl.
- Release и тег: Pimerroc.
- Конфликт: 15 минут обсуждения, затем решает Pimerroc.

## Баланс нагрузки

`Pimerroc` — самое узкое место: agent loop + CI/CD. Поэтому:

- `yel-gar` берёт local Docker, seed, release docs.
- `AX-Ray` берёт ranking, retrieval eval, данные для ranking.
- `krchvl` берёт e2e и demo mode.
- `mrsstrl` берёт demo story и presentation.
- P1 (advanced graph, multi-turn chat, dashboards, native ads) режем первыми.

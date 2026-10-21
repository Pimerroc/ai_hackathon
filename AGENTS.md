# AGENTS.md

Правила для coding-агентов и команды проекта **«Новостная аналитика»** (Alfa Hack 2026).

## 0. Как пользоваться этим файлом

1. Прочитай `AGENTS.md`, затем `.context/README.md`.
2. Перед задачей открой профильный файл в `.context/`: архитектура, API, данные, LLM, quality, demo.
3. Источник правды по задачам — **30 открытых issues** (по одной на человека в день) и мастер-эпик **#54**:
   <https://gitlab.com/dimensia_squad/ai_hackathon/-/issues>
4. Если задачи нет в issue — сначала создай issue или уточни у owner. Не начинай код «из чата».
5. Не меняй чужую зону без review CODEOWNER. Границы — в `.context/team.md`.

## 1. Что строим

Сервис персональной новостной аналитики для руководителей крупного бизнеса:

- определяет контекст компании и группы;
- отбирает значимые внешние события;
- объясняет влияние: риски, возможности, горизонт, уверенность;
- использует аналитику Альфа-Банка с точными цитатами;
- показывает, где факт, где позиция банка, а где вывод AI;
- даёт чат по инсайту и trace действий агента;
- работает как прототип внутри интерфейса Альфа-Бизнеса.

Не делаем обычную новостную ленту и не пересказываем новости одним вызовом LLM.

## 2. Формат сдачи

- Проект отправляется **ZIP-архивом**, не hosted demo.
- Проверяющий разворачивает локально:
  ```bash
  cp .env.example .env
  docker compose up --build
  ```
- Проверяющий, вероятнее всего, использует **свой API-ключ**. `DEMO_MODE=1` должен работать без ключа на precomputed-данных.
- `LIVE_MODE=1` использует реальный LLM.
- В ZIP не должно быть `.env`, ключей, `node_modules`, `.venv`, кэшей и логов.
- Для истории git используем `repo.bundle`, а не полный `.git`.

## 3. Команда и зоны

| Участник | Зона | GitLab |
|---|---|---|
| `Pimerroc` | Agent loop, LLM gateway, CI/CD, tech lead | `@Pimerroc` |
| `AX-Ray` | RAG, ranking, retrieval eval | `@AX-Ray` |
| `yel-gar` | Backend, API, DB, data, local Docker | `@yel-gar` |
| `krchvl` | Frontend | `@krchvl` |
| `mrsstrl` | Design, UX, demo, presentation | `@mrsstrl` |

Правило: **только `Pimerroc` меняет** `.gitlab-ci.yml`, `ci/`, `scripts/package_zip.sh`, теги и release.

## 4. Архитектура в одном экране

```text
News RSS/HTML ─┐
Alpha PDFs ────┼─► ingestion → normalize/dedup → Postgres + pgvector
Company CSV ───┘                                 │
                                                 ├─ company profile + graph
                                                 ├─ news / documents / chunks
                                                 └─ events / insights / evidence
                                                          │
                                              retrieval + ranking
                                                          │
                                              agent runtime (planner/tools/
                                              context/self-check/trace)
                                                          │
                                              FastAPI API → Next.js UI
```

Подробно: `.context/architecture.md`.

## 5. Планируемая структура репозитория

```text
/apps/web                 # Next.js frontend
/services/api             # FastAPI API/BFF
/services/agent           # agent runtime
/services/worker          # ingestion / embeddings / evals
/ml                       # ranking, RAG, prompts, evals
/contracts                # OpenAPI, insight schema, tool schemas
/design                   # tokens, screen specs
/infra                    # docker compose, local runtime
/docs                     # architecture, ADR, demo
/scripts                  # bootstrap, seed, smoke, package_zip
```

Текущий репозиторий — шаблон GitLab CI-компонента. Его нужно заменить продуктовой структурой. Не тащить `templates/my-component.yml` в прод.

## 6. Локальный запуск (целевой контракт)

```bash
cp .env.example .env       # вставить LLM_API_KEY, если нужен LIVE_MODE
docker compose up --build
```

Ожидаемые команды:

```bash
make up          # поднять
make seed        # демо-данные и аккаунты
make smoke       # health + feed + insight + chat + trace
make test        # unit/contract
make demo        # DEMO_MODE без ключа
make verify-zip  # проверка распакованного архива
```

Если команда ещё не реализована — она должна быть создана в соответствующем issue, а не описана только в README.

## 7. LLM

- Base URL: `https://changellenge.up.railway.app/v1`
- API: OpenAI-compatible.
- Ключ: только server-side, только в локальном `.env`, никогда в git, ZIP, логах, frontend и `NEXT_PUBLIC_*`.
- Разрешённые модели — строго из списка в `.context/llm.md`.
- Бюджет: **500 ₽/день на команду**, сброс в **3:00 МСК**.
- При `Budget has been exceeded` — не падать, переходить в `DEMO_MODE` и показывать понятный баннер.
- Все вызовы — через единый gateway с allowlist, кэшем, token/cost accounting и fallback.

## 8. GitLab workflow

- Default branch: `master` (пока; при переименовании обновить этот файл).
- Ветки: `feat/<area>/<issue>-<slug>`, `fix/...`, `docs/...`.
- Коммиты: Conventional Commits.
- MR: ≤ 400 строк, 1 approval, зелёный pipeline, squash merge.
- WIP limit: 1 активный issue на человека.
- Review SLA: 30 минут.
- Milestones: `M0 Foundation` … `M5 Submission`.
- Labels: `type::`, `area::`, `priority::`, `status::`, `day::`.
- Формат issue: подробный бриф — роль, дата, цель, результат, контекст, scope, пошаговый план, артефакты, контракты, DoD, проверка, зависимости/handoff, demo impact, ограничения/cut line, ссылки. Агент читает issue целиком.
- GitHub mirror: <https://github.com/Pimerroc/ai_hackathon> (push mirror GitLab → GitHub).
- Подробно: `.context/workflow.md`.

## 9. Границы, которые нельзя размывать

- Frontend не вызывает LLM напрямую — только API.
- Agent не ходит в БД напрямую — только через tools.
- Backend не содержит prompt’ов — только вызов agent API.
- RAG/ranking не меняет agent state machine.
- CI/CD не трогает никто, кроме `Pimerroc`.
- Секреты не попадают в код, issue, MR, логи и ZIP.

## 10. Definition of Done

- Код + тесты.
- Review CODEOWNER.
- Pipeline green.
- Локальный `docker compose` smoke.
- Документация/ADR обновлена.
- Demo-сценарий не сломан.
- Issue закрыт.

## 11. Текущее состояние

- GitLab: 30 открытых issues + мастер-эпик #54; старые мелкие задачи закрыты как объединённые.
- Репозиторий пока содержит только шаблон CI-компонента.
- Следующие шаги: `#1`, `#3`, `#7`, `#12`, `#13`.
- Полный план и карта issues: `.context/issue-map.md`.

## 12. Если сомневаешься

1. Проверь issue и acceptance criteria.
2. Проверь `.context/architecture.md` и `.context/api.md`.
3. Спроси owner зоны в issue, а не в личке.
4. При конфликте решает `Pimerroc`; архитектурные решения фиксируются в `.context/decisions.md`.

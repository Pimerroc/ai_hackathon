# Карта issues

Формат: **1 issue = 1 человек × 1 день**. Внутри issue — объединённые маленькие задачи. Старые мелкие issues закрыты как объединённые.

- GitLab: <https://gitlab.com/dimensia_squad/ai_hackathon/-/issues>
- Мастер-эпик: **#54**
- Открытых задач: **30**

## M0 · Foundation · 21.10

| Issue | Owner | Задача | Объединено |
|---|---|---|---|
| #1 | Pimerroc | Foundation: contracts, agent skeleton, LLM gateway, CI/security | #2, #9, #10, #11 |
| #3 | yel-gar | Local stack: Compose, OpenAPI, DB/auth, data audit | #4, #5, #6 |
| #7 | mrsstrl | Product frame, design system, hi-fi screens | UX-02 |
| #12 | krchvl | App shell, tokens, mock walking skeleton | — |
| #13 | AX-Ray | RAG foundation: PDF/news parsing, dedup, hybrid retrieval | #14, #15 |

## M1 · First slice · 22.10

| Issue | Owner | Задача | Объединено |
|---|---|---|---|
| #18 | yel-gar | Real data slice: profile, ingestion, feed API | #16, #17 |
| #19 | Pimerroc | Agent slice: tool registry, planner, context memory | #20 |
| #21 | krchvl | Feed and insight detail screens | FE-03 |
| #23 | AX-Ray | Bank citations, retrieval tools, ranking candidates | #24, #25 |
| #35 | mrsstrl | Usability test and design QA | — |

## M2 · MVP · 23.10

| Issue | Owner | Задача | Объединено |
|---|---|---|---|
| #26 | AX-Ray | Ranking v1: scoring, diversity, why-in-feed | #27 |
| #28 | Pimerroc | Agent MVP: self-check, chat, trace | #29, #30 |
| #31 | yel-gar | Insight/chat/trace APIs + demo seed | #43 |
| #32 | krchvl | Provenance, chat UI, trace drawer | #33, #34 |
| #46 | mrsstrl | Demo story and presentation v1 | — |

## M3 · Hardening · 24.10

| Issue | Owner | Задача | Объединено |
|---|---|---|---|
| #8 | mrsstrl | Accessibility, design QA, final screen polish | — |
| #36 | AX-Ray | Noisy data hardening + retrieval fixes | — |
| #38 | Pimerroc | Hardening: guardrails, agent eval, CI, DEMO_MODE | #39, #41, #42 |
| #40 | yel-gar | Observability, audit, local build fixes | — |
| #44 | krchvl | States, filters, feedback, Playwright E2E | — |

## M4 · Release candidate · 25.10

| Issue | Owner | Задача | Объединено |
|---|---|---|---|
| #37 | AX-Ray | Retrieval/ranking eval report + regression gate | — |
| #45 | krchvl | Final UI polish, responsive, demo screenshots | — |
| #47 | Pimerroc | End-to-end integration and demo hardening | — |
| #48 | yel-gar | README, locks, THIRD_PARTY, OpenAPI, architecture | — |
| #51 | mrsstrl | Backup video and final rehearsal | — |

## M5 · Submission · 26.10

| Issue | Owner | Задача | Объединено |
|---|---|---|---|
| #22 | krchvl | Final UI smoke, ZIP bugfixes, submission screenshots | — |
| #49 | Pimerroc | ZIP, repo.bundle, tag v1.0.0, release, submission | #52, #53 |
| #50 | yel-gar | Clean-machine build and ZIP verification | — |
| #55 | AX-Ray | Final retrieval/ranking verification and metrics | — |
| #56 | mrsstrl | Final presentation and submission assets | — |

## Закрытые как объединённые

#2, #4, #5, #6, #9, #10, #11, #14, #15, #16, #17, #20, #24, #25, #27, #29, #30, #33, #34, #39, #41, #42, #43, #52, #53.

## Правило работы

- Один активный issue на человека.
- Внутри issue — чеклист; не создавай отдельный issue на каждую мелкую правку.
- Если задача разрастается — режь P1, а не плоди issues.
- Для синка используем комментарии в дневном issue, а не новые issues.

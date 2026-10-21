# Качество, тесты, CI

## Принцип

Для хакатона важнее воспроизводимость и E2E, чем 100% coverage. Но P0-путь должен быть проверен автоматически и локально.

## Пирамида

- Unit: схемы, ranking features, parsing, utils.
- Contract: OpenAPI, insight schema, tool schemas.
- Integration: API + DB + agent mock, retrieval fixtures.
- E2E: Playwright, 3 демо-сценария на чистом compose.
- Eval: retrieval/ranking и agent quality на golden set.

## Retrieval/ranking eval

- 30–50 golden-запросов.
- Метрики: Recall@10, nDCG@10, citation accuracy.
- Baseline и regression threshold.
- Скрипт `ml/evals/retrieval.py`, report artifact.
- В CI — фикстуры/mock, без реального ключа.

## Agent eval

- 30 golden-кейсов: company × event × expected risks/opportunities.
- LLM-judge rubric + human spot check.
- Метрики: schema validity, citation coverage, groundedness, personalization, bank view, latency, cost.
- Top failures фиксируются в issue; P0 исправляются.

## CI stages

| Stage | Что делает | Блокирует merge |
|---|---|---|
| validate | lint, typecheck, format | да |
| contract | OpenAPI, insight schema, tools | да |
| test | unit/integration | да |
| security | gitleaks, pip-audit/npm audit, Trivy config | да |
| eval:mock | retrieval/agent evals на фикстурах | да |
| e2e | Playwright на compose | да |
| package | ZIP, checksum, repo.bundle | manual/тег |

Без registry, build images, deploy, environments.

> Сейчас в проекте нет активных GitLab runners, поэтому CI/CD отключён на уровне проекта (`builds_access_level=disabled`), а в `.gitlab-ci.yml` стоит `workflow: rules: when: never`. Конфиг готов; включить runner, вернуть `builds_access_level=enabled` и убрать правило в #1.

## Security gates

- gitleaks: ключи, токены, `.env`.
- pip-audit/npm audit: critical/high.
- Trivy config: Docker/compose.
- Проверка, что frontend bundle не содержит `sk-`.
- Проверка, что `.env` не в ZIP.
- Логи не содержат полные prompt’ы/PII.

## Локальная проверка

```bash
cp .env.example .env
docker compose up --build
make seed
make smoke
make test
make e2e
```

Smoke:

- `/healthz`;
- login;
- feed для 3 персон;
- insight из 6 блоков;
- chat с цитатой;
- trace;
- feedback;
- demo mode без ключа.

## ZIP verification

1. Собрать ZIP.
2. Распаковать в чистый temp.
3. `cp .env.example .env`.
4. `docker compose up --build`.
5. Дождаться health.
6. Прогнать smoke и 3 demo-сценария.
7. `docker compose down -v`.
8. Повторить запуск.
9. Проверить checksum и отсутствие секретов.

## Definition of Done

- Код + тесты.
- Review CODEOWNER.
- Pipeline green.
- Локальный compose smoke.
- Docs/ADR обновлены.
- Demo-сценарий не сломан.
- Issue закрыт.

## Что не делаем

- Не гоним полный LLM eval в каждом MR.
- Не строим Docker images в CI.
- Не деплоим.
- Не добавляем тяжёлые фреймворки ради тестов.
- Не блокируем merge на P2-багах.

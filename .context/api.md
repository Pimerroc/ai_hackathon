# API и контракты

## Базовые правила

- API: FastAPI, `/api/v1`.
- Auth: mock JWT для прототипа; в токене `user_id`, `role`, `client_id`.
- Multi-tenant: все запросы фильтруются по `client_id`; пользователь не видит чужого клиента.
- Ошибки: `{ "error": { "code": "...", "message": "...", "details": {} } }`.
- Все ответы с инсайтом валидируются по `contracts/insight.schema.json`.
- Frontend не вызывает LLM и не ходит в БД.

## Endpoints

| Метод | Путь | Назначение |
|---|---|---|
| GET | `/healthz` | health + версия |
| POST | `/auth/mock-login` | demo-пользователь |
| GET | `/clients` | доступные клиенты |
| GET | `/clients/{id}/profile` | профиль, признаки, группа |
| GET | `/clients/{id}/feed` | персональная лента |
| GET | `/events/{id}/insight` | инсайт из 6 блоков |
| POST | `/chat` | вопрос по событию/компании, SSE |
| GET | `/runs/{id}` | trace агента |
| GET | `/sources/{id}` | источник/цитата |
| POST | `/feedback` | оценка инсайта |
| POST | `/admin/ingest` | ручной ingest новости |
| GET | `/metrics` | Prometheus |

## Feed

Query:

- `client_id` (из auth);
- `risk|opportunity|all`;
- `industry`, `region`, `date_from`, `date_to`;
- `page`, `page_size`;
- `sort=rank|date`.

Response:

```json
{
  "items": [
    {
      "event_id": "",
      "title": "",
      "source": "",
      "published_at": "",
      "event_type": "",
      "impact": "risk|opportunity|neutral",
      "confidence": 0.0,
      "why_in_feed": "",
      "has_insight": true
    }
  ],
  "page": 1,
  "total": 0
}
```

## Insight schema

```json
{
  "event_id": "",
  "client_id": "",
  "what_happened": {
    "facts": [{"text": "", "evidence_ids": []}],
    "participants": [],
    "dates": []
  },
  "why_relevant": {
    "company_features": [],
    "links": [{"text": "", "evidence_ids": []}]
  },
  "impact": {
    "risks": [{"text": "", "horizon": "short|mid|long", "confidence": 0.0}],
    "opportunities": [{"text": "", "horizon": "short|mid|long", "confidence": 0.0}]
  },
  "actions": [{"text": "", "priority": "high|medium|low"}],
  "bank_view": {
    "quote": "",
    "document": "",
    "page": 0,
    "label": "bank"
  },
  "sources": [
    {"id": "", "type": "news|bank_pdf", "title": "", "url": "", "quote": ""}
  ],
  "trace": {
    "run_id": "",
    "steps": [],
    "tools": [],
    "model": "",
    "tokens": 0
  },
  "confidence": 0.0,
  "limitations": []
}
```

Правило: каждый ключевой тезис имеет `evidence_ids`; UI показывает бейдж `fact`, `bank`, `AI`, `estimate`.

## Agent tools

| Tool | Вход | Выход |
|---|---|---|
| `get_company_profile` | `client_id` | профиль + признаки |
| `get_group_graph` | `client_id`, `depth` | группа/контрагенты |
| `search_news` | query, filters, top_k | chunks + metadata |
| `search_bank_analytics` | query, topic, top_k | passages + doc/page |
| `get_source` | `source_id` | источник/цитата |
| `rank_events` | `client_id`, candidates | scores + why |
| `save_insight` | insight JSON | id + validation |

Tools read-only. Никаких действий с деньгами/документами.

## Chat

`POST /chat`:

```json
{
  "client_id": "",
  "event_id": "",
  "message": "",
  "history": [{"role": "user|assistant", "content": ""}]
}
```

Ответ — `text/event-stream`: `thinking`, `token`, `citation`, `done`, `error`.

## Trace

`GET /runs/{id}`:

```json
{
  "run_id": "",
  "model": "",
  "status": "success|failed",
  "steps": [
    {"name": "plan", "status": "ok", "latency_ms": 0},
    {"name": "tool:search_news", "input_summary": "", "output_summary": "", "latency_ms": 0}
  ],
  "tokens": 0,
  "cost_rub": 0.0,
  "evidence": []
}
```

## Feedback

```json
{
  "insight_id": "",
  "rating": "up|down",
  "reason": "irrelevant|wrong_fact|bad_bank_view|other",
  "comment": ""
}
```

## Contract rules

- OpenAPI — источник правды для frontend/API.
- Изменение контракта — отдельный MR с обновлением `contracts/` и `.context/api.md`.
- Contract tests в CI.
- Mock server обновляется в том же MR.
- Frontend не парсит «сырой» текст LLM; только structured JSON.

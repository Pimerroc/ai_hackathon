# LLM и бюджет

## Подключение

- API: OpenAI-compatible.
- Base URL: `https://changellenge.up.railway.app/v1`
- API Key: выдаётся команде, начинается с `sk-...`.
- Ключ хранится только в локальном `.env`.
- В публичный репозиторий, ZIP, issue, MR, логи и frontend ключ не попадает.

## Разрешённые модели

| Model ID | Для чего |
|---|---|
| `google/gemma-4-26b-a4b-it` | классификация, NER, теги, дедуп, простые преобразования |
| `qwen/qwen3.6-35b-a3b` | извлечение, суммаризация, structured JSON |
| `z-ai/glm-5.3-flash` | сложное рассуждение о влиянии, critic |
| `deepseek/deepseek-v4.1-flash` | research, кросс-документный анализ, длинный контекст |
| `moonshotai/kimi-k2.6` | длинные аналитические тексты |
| `qwen/qwen3-vl-30b-a3b-instruct` | PDF-страницы с таблицами/графиками |

Другие модели запрещены. Названия копировать точно.

## `.env.example`

```dotenv
LLM_API_KEY=sk-...
LLM_BASE_URL=https://changellenge.up.railway.app/v1

LLM_MODEL_DEFAULT=deepseek/deepseek-v4.1-flash
LLM_MODEL_CLASSIFY=google/gemma-4-26b-a4b-it
LLM_MODEL_EXTRACT=qwen/qwen3.6-35b-a3b
LLM_MODEL_REASON=z-ai/glm-5.3-flash
LLM_MODEL_RESEARCH=deepseek/deepseek-v4.1-flash
LLM_MODEL_LONG=moonshotai/kimi-k2.6
LLM_MODEL_VISION=qwen/qwen3-vl-30b-a3b-instruct

DAILY_BUDGET_RUB=500
BUDGET_TIMEZONE=Europe/Moscow
BUDGET_RESET_HOUR=3
```

## Gateway

Все вызовы идут через `llm_gateway`:

- allowlist моделей при старте;
- JSON mode;
- retries/timeout;
- token/cost accounting;
- Redis-кэш;
- fallback между моделями;
- daily budget guard;
- логирование run_id, модели, токенов, latency без ключа и PII.

## Бюджет

- 500 ₽/день на один ключ, общий на команду и все модели.
- Сброс в 3:00 МСК.
- При `Budget has been exceeded`:
  1. не падать;
  2. переключиться на `DEMO_MODE` с precomputed insights;
  3. показать баннер «Дневной лимит исчерпан, демо-режим; сброс в 3:00 МСК»;
  4. продолжить демо без live-вызовов.

## Экономия

- Precompute инсайтов для демо.
- Кэш ответов и эмбеддингов.
- Малые модели для рутины, большие — только для финальной интерпретации.
- Ограничение top-k чанков и max tokens.
- Полный eval — локально/nightly, не в каждом MR.
- В CI — только mock/fixture evals, без реального ключа.

## Безопасность

- Ключ только server-side.
- Никаких `NEXT_PUBLIC_*` с ключом.
- gitleaks в CI.
- Не логировать полные prompt’ы и ответы с чувствительными данными.
- Prompt injection: новости — недоверенный контент, tools — allowlist, output — schema validation.
- Rate limit, timeout, circuit breaker.

## Ошибки

| Ошибка | Поведение |
|---|---|
| `Budget has been exceeded` | DEMO_MODE + баннер, без падения |
| 401/403 | понятная ошибка «проверьте LLM_API_KEY» |
| timeout | retry 1–2 раза, затем fallback |
| schema invalid | critic/repair, затем safe failure |
| model unavailable | fallback на разрешённую модель |

---
tags: [microservices, observability, tracing, infrastructure]
sources: [Прочие_Реже встречающиеся вопросы технических собеседований.pdf]
---

# Distributed Tracing — Zipkin, Jaeger

## 1. Проблема — зачем это существует?

В монолите упавший запрос виден в одном стектрейсе. В микросервисах запрос проходит через 5–10 сервисов: API Gateway → Order → Payment → Inventory → Notification. Если пользователь жалуется на «долгий заказ» — в каком сервисе узкое место? Обычные логи в каждом сервисе не помогут: они разрозненные, нет единого view на «путь» конкретного запроса. Distributed Tracing решает это — показывает полный путь запроса через все сервисы с таймингами на каждом шаге.

## 2. Аналогия

Курьерская доставка с отслеживанием: посылка проходит склад отправителя → сортировочный центр → транспорт → склад получателя → курьер → доставлено. На каждом этапе сканируется штрихкод с временной меткой. Если посылка задержалась — видно где именно.

Distributed Tracing — это штрихкод (Trace ID), который путешествует с запросом через все сервисы.

## 3. Как работает

### Ключевые понятия

**Trace** — весь путь одного запроса от начала до конца (один штрихкод).

**Span** — один отрезок работы в одном сервисе (один этап сортировки). Содержит: название операции, start time, duration, теги (HTTP status, DB query), logs.

**Trace ID** — уникальный ID всего пути. Передаётся в HTTP-заголовке между сервисами.

**Parent Span ID** — кто вызвал текущий span (иерархия вызовов).

```
Trace ID: abc-123
│
├── Span: API Gateway [0ms — 250ms]
│   ├── Span: OrderService [5ms — 200ms]
│   │   ├── Span: DB query [10ms — 50ms]
│   │   └── Span: PaymentService [60ms — 180ms]
│   │       ├── Span: Stripe API [70ms — 160ms]  ← узкое место!
│   │       └── Span: DB write [165ms — 175ms]
│   └── Span: NotificationService [205ms — 245ms]
```

---

### Spring Boot + Micrometer Tracing (Zipkin)

```xml
<!-- pom.xml -->
<dependency>
    <groupId>io.micrometer</groupId>
    <artifactId>micrometer-tracing-bridge-brave</artifactId>
</dependency>
<dependency>
    <groupId>io.zipkin.reporter2</groupId>
    <artifactId>zipkin-reporter-brave</artifactId>
</dependency>
```

```yaml
# application.yml
management:
  tracing:
    sampling:
      probability: 1.0   # 100% запросов (в prod — 0.1 = 10%)
spring:
  zipkin:
    base-url: http://zipkin:9411
```

После этого Spring автоматически:
- Генерирует `traceId` для входящего запроса
- Передаёт `traceId` и `spanId` в заголовках `traceparent` (W3C) или `X-B3-*` (Zipkin B3)
- Отправляет spans в Zipkin/Jaeger

---

### Zipkin vs Jaeger

| | Zipkin | Jaeger |
|--|--------|--------|
| Создан | Twitter | Uber |
| Хранение | In-memory, MySQL, Cassandra, ES | Cassandra, ES |
| UI | Простой | Богаче (DAG, dependency graph) |
| Интеграция | Spring Sleuth / Micrometer | OpenTelemetry |
| Когда | Простые проекты, быстрый старт | Enterprise, сложные системы |

Оба поддерживают **OpenTelemetry** — стандарт для инструментации (vendor-neutral).

---

### Propagation — как Trace ID передаётся

```
HTTP Headers:
  traceparent: 00-abc123def456-span789-01
               version-traceId-parentSpanId-flags

# или Zipkin B3:
  X-B3-TraceId: abc123
  X-B3-SpanId: def456
  X-B3-ParentSpanId: bbb111
```

Каждый сервис читает эти заголовки, создаёт дочерний span, и передаёт дальше при вызове следующего сервиса.

## 4. Глубже — что важно знать

**Sampling — нельзя трасировать 100% в prod.** При высокой нагрузке (1000 rps) трасировка каждого запроса создаёт огромный объём данных. В production: `probability: 0.01` (1%) или **adaptive sampling** — 100% ошибочных запросов + 1% нормальных.

**Корреляция с логами.** В Logback/Log4j2 добавляем `traceId` и `spanId` в MDC — тогда логи автоматически содержат эти ID:

```yaml
logging:
  pattern:
    level: "%5p [${spring.application.name},%X{traceId},%X{spanId}]"
```

Теперь в Kibana/Grafana Loki можно найти все логи конкретного запроса по `traceId`.

**Три столпа observability:**
- **Metrics** (Prometheus/Grafana) — агрегированные числа: RPS, latency p99, error rate
- **Logs** (ELK/Loki) — детали конкретных событий
- **Traces** (Zipkin/Jaeger) — путь конкретного запроса через сервисы

Трасировка дополняет метрики: метрики показывают «в PaymentService высокая latency», трасировка показывает «вот конкретный запрос, и вот почему».

## 5. Связи с другими концепциями

- [[Микросервисы vs монолит]] — distributed tracing — необходимый инструмент для отладки в микросервисах
- [[Service Discovery Config Server]] — трасировка помогает понять какой инстанс сервиса обработал запрос
- [[Kafka топики, партиции, офсеты, брокеры, consumer group]] — трасировка через Kafka: Kafka spans в Micrometer

## 6. Ответ на собесе (2 минуты)

В микросервисах запрос проходит через множество сервисов. Когда пользователь жалуется на медленный ответ — обычные логи не помогают: они разрозненные. Distributed Tracing решает это: каждый запрос получает уникальный **Trace ID**, который передаётся в HTTP-заголовках между всеми сервисами.

Каждый сервис создаёт **Span** — отрезок своей работы с таймингом. Spans образуют дерево, визуализируя полный путь запроса с временем на каждом шаге. Zipkin и Jaeger — это UI для просмотра этих деревьев и поиска узких мест.

В Spring Boot это работает через Micrometer Tracing: добавил зависимости, указал URL Zipkin — и трасировка работает автоматически. В production использую sampling 1–10% запросов, но всегда 100% ошибочных.

Важная практика — добавить `traceId` в паттерн логирования. Тогда в Kibana можно найти все логи конкретного запроса по его traceId.

## Шпаргалка

| Понятие | Что это |
|---------|---------|
| Trace | Полный путь запроса (один ID) |
| Span | Один шаг в одном сервисе |
| Trace ID | Уникальный ID, путешествует в заголовках |
| Parent Span | Кто вызвал данный span |

| | Zipkin | Jaeger |
|--|--------|--------|
| Создан | Twitter | Uber |
| Complexity | Проще | Богаче (DAG, dependency graph) |
| Стандарт | B3 / OpenTelemetry | OpenTelemetry |

**Связи:**
- [[Микросервисы vs монолит]]
- [[Service Discovery Config Server]]

---
tags: [microservices, http, rest, soap, api]
sources: [Прочие_Реже встречающиеся вопросы технических собеседований.pdf]
---

# SOAP vs REST, WSDL

## 1. Проблема — зачем это существует?

Системы должны общаться через сеть по стандартному протоколу. SOAP (Simple Object Access Protocol) — строгий стандарт с XML, схемой (WSDL), встроенными гарантиями безопасности и транзакций. REST — лёгкий архитектурный стиль поверх HTTP, без жёсткой схемы, с JSON. Современные API используют REST (или gRPC), SOAP — в legacy enterprise и банковском секторе. На собесе спрашивают, чтобы понять, знаешь ли ты откуда растут ноги у REST.

## 2. Аналогия

**SOAP** — официальная бумажная переписка с гербовой печатью, строгим форматом, описью вложений (WSDL), подписью и нотариальным заверением. Долго, надёжно, юридически значимо.

**REST** — мессенджер: быстро, свободный формат, читаемо, удобно. Нет встроенных гарантий, зато работаешь с любого устройства.

## 3. Как работает

### SOAP — структура

```xml
<!-- SOAP Request: получить баланс -->
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Header>
        <auth:Security>
            <auth:UsernameToken>
                <auth:Username>user</auth:Username>
                <auth:Password>pass</auth:Password>
            </auth:UsernameToken>
        </auth:Security>
    </soap:Header>
    <soap:Body>
        <bank:GetBalance>
            <bank:AccountId>12345</bank:AccountId>
        </bank:GetBalance>
    </soap:Body>
</soap:Envelope>
```

**WSDL (Web Service Description Language)** — XML-схема, описывающая весь контракт сервиса: какие методы есть, какие параметры принимают, что возвращают. Клиент генерирует код из WSDL автоматически.

```xml
<!-- Фрагмент WSDL -->
<wsdl:operation name="GetBalance">
    <wsdl:input message="tns:GetBalanceRequest"/>
    <wsdl:output message="tns:GetBalanceResponse"/>
</wsdl:operation>
```

---

### REST — структура

```
GET /accounts/12345/balance
Authorization: Bearer eyJhbGc...

200 OK
{
  "accountId": "12345",
  "balance": 1500.00,
  "currency": "RUB"
}
```

REST — архитектурный стиль (не протокол), основанный на HTTP. Принципы REST по Fielding:
1. **Stateless** — сервер не хранит состояние клиента между запросами
2. **Uniform Interface** — стандартные HTTP-методы + URI как ресурс
3. **Client-Server** — разделение ответственности
4. **Cacheable** — ответы могут кэшироваться
5. **Layered System** — клиент не знает, через сколько прокси идёт запрос

---

### Сравнение SOAP vs REST

| | SOAP | REST |
|--|------|------|
| Протокол | SOAP over HTTP/SMTP/TCP | HTTP |
| Формат | XML (всегда) | JSON, XML, любой |
| Контракт | WSDL (строгий) | OpenAPI/Swagger (опциональный) |
| Безопасность | WS-Security (встроенная) | OAuth2/JWT (внешняя) |
| Транзакции | WS-AtomicTransaction (встроенные) | Нет (нужно реализовывать) |
| Сложность | Высокая | Низкая |
| Производительность | Медленнее (XML тяжёлый) | Быстрее (JSON лёгкий) |
| Stateful | Может быть | Stateless |
| Где применяется | Банки, legacy enterprise, 1С | Современные API, мобильные, веб |

---

### JSON-RPC — упоминание

**JSON-RPC** — упрощённый RPC-протокол поверх HTTP (или WebSocket). В отличие от REST, URL всегда один, метод передаётся в теле запроса.

```json
// Запрос
POST /api
{
  "jsonrpc": "2.0",
  "method": "getBalance",
  "params": {"accountId": "12345"},
  "id": 1
}

// Ответ
{
  "jsonrpc": "2.0",
  "result": {"balance": 1500.00},
  "id": 1
}
```

Применяется в: Ethereum API, некоторых banking API. Проще SOAP, но менее RESTful.

## 4. Глубже — что важно знать

**Когда SOAP всё ещё используется:**
- Банки и финансы (требования регуляторов к WS-Security и транзакциям)
- Интеграция с legacy enterprise-системами (SAP, 1С)
- Системы, где строгий контракт с кодогенерацией критичен

**gRPC как альтернатива и SOAP, и REST:**
- Protobuf вместо XML/JSON (компактнее, быстрее)
- Строгий контракт в `.proto` файле (как WSDL, но лучше)
- HTTP/2 (мультиплексирование)
- Streaming
- Применяется: внутренние микросервисы, gRPC-gateway для публичного API

## 5. Связи с другими концепциями

- [[Разница HTTP методов]] — REST построен на HTTP-методах
- [[PUT vs PATCH, идемпотентность HTTP-методов]] — идемпотентность — ключевой принцип REST
- [[Синхронное и асинхронное взаимодействие в микросервисах]] — REST = синхронный способ взаимодействия

## 6. Ответ на собесе (2 минуты)

SOAP — протокол обмена сообщениями на XML с жёстким контрактом WSDL. Контракт описывает все методы, параметры и типы — клиент генерирует код автоматически. Встроенные: безопасность (WS-Security), транзакции (WS-AtomicTransaction). Применяется в банках и legacy-системах, где требования регуляторов или строгие контракты.

REST — архитектурный стиль поверх HTTP. Ресурсы — URI, действия — HTTP-методы (GET/POST/PUT/DELETE), формат — обычно JSON. Stateless: сервер не хранит состояние между запросами. Легче, быстрее, широко принят для веб и мобильных API.

Ключевые отличия: SOAP — тяжёлый XML + встроенные гарантии, REST — лёгкий JSON + простота. В новых проектах — REST или gRPC. SOAP — только для интеграции с legacy.

## Шпаргалка

| | SOAP | REST | gRPC |
|--|------|------|------|
| **Формат** | XML | JSON | Protobuf |
| **Контракт** | WSDL | OpenAPI | .proto |
| **Транспорт** | HTTP/SMTP/TCP | HTTP/1.1 | HTTP/2 |
| **Безопасность** | WS-Security | OAuth2/JWT | TLS + OAuth2 |
| **Где** | Банки, legacy | Веб, мобильные | Внутренние сервисы |

**Связи:**
- [[Разница HTTP методов]]
- [[PUT vs PATCH, идемпотентность HTTP-методов]]

**Hexlet:**
- [[HTTP API]]
- [[Протокол HTTP]]

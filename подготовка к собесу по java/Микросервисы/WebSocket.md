---
tags: [microservices, websocket, http, networking]
sources: [Прочие_Реже встречающиеся вопросы технических собеседований.pdf]
---

# WebSocket — для чего используется

## 1. Проблема — зачем это существует?

HTTP работает по модели «запрос → ответ»: клиент всегда инициирует, сервер только отвечает. Чтобы получить обновления от сервера, клиент вынужден постоянно опрашивать (polling): «Есть новые сообщения? Нет. Есть? Нет. Есть? Да.» — это wasteful и медленно. WebSocket устанавливает постоянное двустороннее соединение: сервер может **сам пушить данные** клиенту без запроса.

## 2. Аналогия

HTTP — как посещение почты: каждый раз приходишь, спрашиваешь «есть письма?», получаешь ответ, уходишь. Если хочешь узнать быстро — нужно часто приходить.

WebSocket — как телефонная линия, которая остаётся открытой: один раз соединился, и обе стороны могут говорить в любой момент без нового звонка.

## 3. Как работает

### Handshake — переход с HTTP на WebSocket

```
Клиент → Сервер:
GET /chat HTTP/1.1
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==

Сервер → Клиент:
HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=
```

После этого — постоянный TCP-канал, HTTP больше не используется. Соединение живёт, пока не закроют вручную.

---

### Spring WebSocket (STOMP)

```java
@Configuration
@EnableWebSocketMessageBroker
public class WebSocketConfig implements WebSocketMessageBrokerConfigurer {

    @Override
    public void registerStompEndpoints(StompEndpointRegistry registry) {
        registry.addEndpoint("/ws").withSockJS();  // /ws — точка подключения
    }

    @Override
    public void configureMessageBroker(MessageBrokerRegistry registry) {
        registry.enableSimpleBroker("/topic");        // сервер пушит сюда
        registry.setApplicationDestinationPrefixes("/app"); // клиент шлёт сюда
    }
}

@Controller
public class ChatController {

    @MessageMapping("/chat.send")        // клиент шлёт на /app/chat.send
    @SendTo("/topic/chat")               // сервер broadcast всем подписчикам /topic/chat
    public ChatMessage send(ChatMessage msg) {
        return msg;
    }
}
```

```javascript
// Клиент (JS)
const socket = new SockJS('/ws');
const stompClient = Stomp.over(socket);
stompClient.connect({}, () => {
    stompClient.subscribe('/topic/chat', (msg) => {
        console.log(JSON.parse(msg.body));
    });
    stompClient.send('/app/chat.send', {}, JSON.stringify({text: 'Hello'}));
});
```

---

### Когда WebSocket, а когда HTTP

| Критерий | HTTP | WebSocket |
|----------|------|-----------|
| Направление | Клиент → Сервер | Двустороннее |
| Соединение | Новое на каждый запрос | Постоянное |
| Нагрузка на сервер | Ниже (stateless) | Выше (держит соединения) |
| Use case | CRUD, REST API | Real-time, live updates |

**Когда WebSocket:**
- Чат (мгновенная доставка сообщений)
- Онлайн-игры (real-time состояние)
- Live-дашборды (биржевые котировки, мониторинг)
- Уведомления (push без polling)
- Совместное редактирование (Google Docs-стиль)

**Когда НЕ нужен WebSocket:**
- Обычные CRUD-операции
- Редкие обновления (раз в минуту достаточно polling или SSE)
- Масштабирование на много инстансов — WebSocket stateful, нужны sticky sessions или Redis Pub/Sub

## 4. Глубже — что важно знать

**SSE (Server-Sent Events)** — упрощённая альтернатива для одностороннего потока сервер → клиент. Работает поверх обычного HTTP, проще в реализации, но только сервер пушит.

```java
@GetMapping(value = "/events", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
public Flux<String> events() {
    return Flux.interval(Duration.ofSeconds(1)).map(i -> "event " + i);
}
```

**Масштабирование WebSocket:** при нескольких инстансах сервера клиент подключён к одному, а сообщение может прийти в другой. Решение: **Redis Pub/Sub** или **RabbitMQ** как общий брокер для рассылки между инстансами.

**WebSocket vs Polling:**
- Short polling: запрос каждые N секунд — простой, много бесполезных запросов
- Long polling: запрос висит до появления данных — лучше, но всё ещё накладно
- WebSocket: одно соединение, данные приходят когда есть

## 5. Связи с другими концепциями

- [[Разница HTTP методов]] — WebSocket начинается с HTTP upgrade, но затем выходит за рамки HTTP
- [[Синхронное и асинхронное взаимодействие в микросервисах]] — WebSocket — асинхронный push от сервера к клиенту
- [[Kafka топики, партиции, офсеты, брокеры, consumer group]] — Kafka → WebSocket: типичная цепочка для real-time дашбордов

## 6. Ответ на собесе (2 минуты)

WebSocket решает проблему HTTP: клиент не может получать данные от сервера без запроса. Без WebSocket нужен polling — частые запросы «есть новое?», которые расходуют ресурсы.

WebSocket начинается с HTTP-запроса с заголовком `Upgrade: websocket`. Сервер отвечает `101 Switching Protocols`, и между ними остаётся постоянный TCP-канал. Теперь обе стороны могут отправлять данные в любой момент.

Применяется для: чата, live-дашбордов, онлайн-игр, push-уведомлений — везде, где нужен real-time поток с сервера на клиент.

Нюанс масштабирования: WebSocket stateful — клиент привязан к конкретному инстансу. При нескольких серверах нужен Redis Pub/Sub или STOMP-брокер, чтобы рассылать сообщения всем подключённым клиентам независимо от инстанса.

## Шпаргалка

| | HTTP | WebSocket | SSE |
|--|------|-----------|-----|
| **Инициатор** | Клиент | Оба | Сервер |
| **Соединение** | Новое | Постоянное | Постоянное |
| **Направление** | Request-Response | Двустороннее | Сервер → Клиент |
| **Use case** | CRUD | Чат, игры | Уведомления, дашборды |

**Связи:**
- [[Разница HTTP методов]]
- [[Синхронное и асинхронное взаимодействие в микросервисах]]

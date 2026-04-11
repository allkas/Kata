---
tags: [spring, aop, proxy]
---
# Spring AOP
## 1. AOP в Spring
**Aspect** — модуль с перекрестной логикой (логирование, транзакции).
**Join point** — точка вызова.
**Advice** — что и когда выполнять.
**Pointcut** — выражение, выбирающее join point.
## 2. JDK proxy vs CGLIB proxy
- **JDK proxy** — для интерфейсов (требует implements).
- **CGLIB** — для классов (создает подкласс). Spring выбирает автоматически.
## 3. Проксирование @Transactional
Spring создаёт прокси, который открывает/закрывает транзакцию до/после вызова метода.
**Связи:**
- [[Транзакции уровни изоляции]]
- [[Spring Core IoC DI]]
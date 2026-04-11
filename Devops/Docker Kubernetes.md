---
tags: [docker, kubernetes, containers]
---
# Docker / Kubernetes
## Docker vs VM
- **VM** — своя ОС, гипервизор, гигабайты.
- **Docker** — общее ядро, изоляция, мегабайты.
## Dockerfile
```dockerfile
FROM openjdk:17
COPY target/app.jar app.jar
CMD ["java", "-jar", "app.jar"]
```
## Kubernetes

- **Pod** — один или несколько контейнеров.
    
- **Deployment** — управление репликами.
    
- **Service** — стабильный доступ к Pod'ам.
    

**Связи:**

- [[Микросервисы vs монолит]]
    
- [[Maven жизненный цикл]]
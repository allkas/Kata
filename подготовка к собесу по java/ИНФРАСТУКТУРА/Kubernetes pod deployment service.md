---
tags: [kubernetes, k8s, devops, containers, infrastructure]
sources: [DevOps И ИНФРАСТУКТУРА Вопросы технических собеседований.pdf]
---

# Kubernetes: pod, deployment, service

## 1. Проблема — зачем это существует?

Один контейнер на одном хосте — просто Docker. Но в production нужно: перезапуск при падении, масштабирование под нагрузку, обновление без downtime, балансировка трафика между копиями. Kubernetes — оркестратор, который автоматизирует всё это: декларируешь желаемое состояние (`replicas: 3`), Kubernetes следит, чтобы оно всегда выполнялось.

## 2. Аналогия

**Pod** — рабочая бригада (1–2 человека с общим инструментом).

**Deployment** — HR-менеджер бригад: знает, что бригад нужно всегда 3. Если одна заболела — нанимает новую. Если нужно обучить новому навыку — заменяет по одной, не останавливая работу.

**Service** — ресепшн: у него всегда один адрес и номер телефона, независимо от того, какие конкретно бригады сейчас работают внутри. Клиент не знает про внутреннюю ротацию.

## 3. Как работает

### Pod — минимальная единица

Pod = один или несколько контейнеров, которые делят сеть и storage. Каждый Pod получает свой IP внутри кластера.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-app
spec:
  containers:
  - name: app
    image: my-app:1.0.0
    ports:
    - containerPort: 8080
    resources:
      requests:
        memory: "256Mi"
        cpu: "250m"
      limits:
        memory: "512Mi"
        cpu: "500m"
```

Pods не создают вручную в production — они эфемерны. Создают через Deployment.

---

### Deployment — управление репликами и обновлениями

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 3          # всегда 3 копии
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: app
        image: my-app:1.0.0
        ports:
        - containerPort: 8080
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1        # можно создать +1 сверх replicas
      maxUnavailable: 0  # ни один Pod не недоступен во время обновления
```

**Rolling Update** — обновление без downtime: Kubernetes создаёт новые Pods с новой версией, убивает старые по одному. `maxUnavailable: 0` гарантирует, что всегда есть рабочие копии.

---

### Service — стабильный сетевой адрес

Pods умирают и рождаются — их IP меняется. Service — постоянный виртуальный IP с балансировкой по label selector.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-app-service
spec:
  selector:
    app: my-app           # все Pods с этим лейблом
  ports:
  - port: 80              # порт Service
    targetPort: 8080      # порт в Pod
  type: ClusterIP         # только внутри кластера
```

**Типы Service:**

| Тип | Доступность | Когда |
|-----|-------------|-------|
| `ClusterIP` | Только внутри кластера | Между микросервисами |
| `NodePort` | Через IP ноды + порт | Дев/тест, простой внешний доступ |
| `LoadBalancer` | Внешний IP от cloud | Production внешний трафик |

---

### Связь компонентов

```
Интернет
    ↓
Service (ClusterIP/LoadBalancer) ← стабильный адрес
    ↓ балансировка по label selector
Pod A (app=my-app)
Pod B (app=my-app)   ← Deployment управляет всеми тремя
Pod C (app=my-app)
```

## 4. Глубже — что важно знать

**ReplicaSet** — низкоуровневый ресурс, который поддерживает нужное количество Pod. Deployment создаёт ReplicaSet автоматически. Напрямую ReplicaSet не создают.

**Readiness vs Liveness probe:**
```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8080
  initialDelaySeconds: 30   # подождать 30с перед первой проверкой
  periodSeconds: 10         # проверять каждые 10с
  # Если fail — Pod перезапускается

readinessProbe:
  httpGet:
    path: /ready
    port: 8080
  # Если fail — Pod убирается из Service (не получает трафик), но не перезапускается
```

**Разница probe:** `liveness` — жив ли процесс (перезапуск при отказе). `readiness` — готов ли принимать трафик (убирает из ротации при отказе, не убивает).

**ConfigMap и Secret:**
```yaml
env:
- name: DB_URL
  valueFrom:
    configMapKeyRef:
      name: app-config
      key: db.url
- name: DB_PASSWORD
  valueFrom:
    secretKeyRef:
      name: app-secrets
      key: db.password
```

**Аналогия с Service Discovery (Eureka):** Kubernetes Service — это встроенный service discovery. Вместо Eureka сервисы находят друг друга по DNS: `http://my-app-service:80`. Kubernetes DNS резолвит имя сервиса в его ClusterIP.

## 5. Связи с другими концепциями

- [[Dockerfile и слои образа]] — образ, который деплоится в Pod
- [[Docker vs VM]] — Docker-контейнер внутри Pod
- [[Service Discovery Config Server]] — Kubernetes Service vs Eureka — разные уровни abstraction
- [[Микросервисы vs монолит]] — Kubernetes — типичная платформа для микросервисов

## 6. Ответ на собесе (2 минуты)

Kubernetes работает с тремя ключевыми абстракциями.

**Pod** — минимальная единица: один или несколько контейнеров, которые делят сеть. Pods эфемерны — умирают и создаются заново, у них меняются IP.

**Deployment** — управляет репликами Pods. Ты декларируешь `replicas: 3`, Kubernetes следит, чтобы всегда было три живых Pod. При обновлении образа Deployment делает Rolling Update: создаёт новые по одному, убивает старые, без downtime.

**Service** — постоянный сетевой адрес для группы Pods. Выбирает Pods по label selector, балансирует трафик. Внутри кластера сервисы находят друг друга по DNS: `http://payment-service:8080`. Это встроенный service discovery, вместо Eureka.

Лучшая практика: всегда добавлять `readinessProbe` — иначе Kubernetes пустит трафик на Pod, который ещё не готов к работе.

## Шпаргалка

| Компонент | Аналогия | Что делает |
|-----------|----------|-----------|
| Pod | Рабочая бригада | 1+ контейнеров, общая сеть |
| Deployment | HR-менеджер | Поддерживает N реплик, rolling update |
| ReplicaSet | Исполнитель Deployment | Следит за количеством Pods |
| Service | Ресепшн | Стабильный IP, балансировка по лейблам |

| Probe | Действие при fail | Зачем |
|-------|------------------|-------|
| `livenessProbe` | Перезапуск Pod | Обнаружить зависший процесс |
| `readinessProbe` | Убрать из Service | Не пускать трафик до готовности |

| Service тип | Доступен |
|-------------|---------|
| ClusterIP | Только внутри кластера |
| NodePort | IP ноды + port |
| LoadBalancer | Внешний IP от cloud provider |

**Связи:**
- [[Dockerfile и слои образа]]
- [[Docker vs VM]]
- [[Service Discovery Config Server]]

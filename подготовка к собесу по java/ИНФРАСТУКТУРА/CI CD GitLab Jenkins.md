---
tags: [devops, cicd, gitlab, jenkins, infrastructure]
sources: [Прочие_Реже встречающиеся вопросы технических собеседований.pdf]
---

# CI/CD — GitLab CI, Jenkins

## 1. Проблема — зачем это существует?

Без CI/CD: разработчик делает `git push`, потом вручную запускает тесты, вручную собирает jar, вручную деплоит на сервер. Это медленно, ошибкоёмко и «работает на моей машине». CI/CD автоматизирует весь путь кода от коммита до production: тесты запускаются автоматически, образы собираются, деплой происходит без ручного вмешательства.

## 2. Аналогия

Конвейер на заводе: деталь попала на ленту → автоматически проверяется на прочность → красится → упаковывается → отправляется. Никто не переносит деталь вручную между этапами. Если на проверке дефект — деталь отбраковывается, конвейер не останавливается.

CI/CD — конвейер для кода: коммит → тесты → сборка → деплой на staging → деплой на prod.

## 3. Как работает

### CI (Continuous Integration) — непрерывная интеграция

Каждый `git push` или PR запускает пайплайн:
1. **Checkout** — скачать код
2. **Build** — скомпилировать (`mvn compile`)
3. **Test** — запустить unit + integration тесты
4. **Static analysis** — SonarQube, Checkstyle, SpotBugs
5. **Build artifact** — собрать jar/Docker image

**Цель:** быстро узнать, что коммит не сломал сборку и тесты.

### CD (Continuous Delivery/Deployment) — непрерывная доставка

- **Continuous Delivery:** артефакт готов к деплою, но деплой в prod — по нажатию кнопки (ручное подтверждение)
- **Continuous Deployment:** деплой в prod полностью автоматически, без ручного шага

---

### GitLab CI — файл `.gitlab-ci.yml`

```yaml
stages:
  - build
  - test
  - docker
  - deploy

variables:
  MAVEN_OPTS: "-Dmaven.repo.local=.m2/repository"

# Кэшировать maven-зависимости между запусками
cache:
  paths:
    - .m2/repository

build:
  stage: build
  image: maven:3.9-eclipse-temurin-17
  script:
    - mvn compile -DskipTests

test:
  stage: test
  image: maven:3.9-eclipse-temurin-17
  script:
    - mvn test
  artifacts:
    reports:
      junit: target/surefire-reports/*.xml

docker-build:
  stage: docker
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  only:
    - main

deploy-staging:
  stage: deploy
  script:
    - kubectl set image deployment/my-app app=$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  environment:
    name: staging
  only:
    - main

deploy-prod:
  stage: deploy
  script:
    - kubectl set image deployment/my-app app=$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  environment:
    name: production
  when: manual   # ← деплой в prod только по кнопке
  only:
    - tags
```

---

### Jenkins — Jenkinsfile (declarative pipeline)

```groovy
pipeline {
    agent any

    tools {
        maven 'Maven 3.9'
        jdk 'JDK 17'
    }

    stages {
        stage('Build') {
            steps {
                sh 'mvn compile -DskipTests'
            }
        }
        stage('Test') {
            steps {
                sh 'mvn test'
            }
            post {
                always {
                    junit 'target/surefire-reports/*.xml'
                }
            }
        }
        stage('Docker Build') {
            steps {
                script {
                    def image = docker.build("my-app:${env.BUILD_NUMBER}")
                    docker.withRegistry('https://registry.example.com') {
                        image.push()
                    }
                }
            }
        }
        stage('Deploy Prod') {
            when {
                branch 'main'
            }
            input {
                message "Deploy to production?"
            }
            steps {
                sh "kubectl set image deployment/my-app app=registry.example.com/my-app:${env.BUILD_NUMBER}"
            }
        }
    }
}
```

---

### GitLab CI vs Jenkins

| | GitLab CI | Jenkins |
|--|-----------|---------|
| Настройка | YAML в репозитории | Jenkinsfile / UI |
| Интеграция | Встроена в GitLab | Отдельный сервер |
| Экосистема | GitLab-focused | Тысячи плагинов |
| Инфраструктура | GitLab Runners | Jenkins Agents |
| Кривая обучения | Ниже | Выше |
| Гибкость | Хорошая | Очень высокая |
| Когда | Новые проекты на GitLab | Legacy, сложные цепочки |

## 4. Глубже — что важно знать

**Environments и approvals:** prod-деплой требует ручного подтверждения (`when: manual` в GitLab, `input` в Jenkins). Это граница между Continuous Delivery и Continuous Deployment.

**Secrets/Variables:** пароли, токены никогда не в коде. В GitLab — CI/CD Variables (Masked). В Jenkins — Credentials store. Используются через переменные окружения.

**Артефакты и кэш:**
- **Артефакт** — файл, который передаётся между стадиями (jar, Docker image)
- **Кэш** — сохраняется между запусками (maven repo, node_modules) — ускоряет сборку

**GitLab Runners:** агенты, которые выполняют jobs. Могут быть shared (бесплатные от GitLab), group или specific (свои серверы). Каждый job — изолированный контейнер.

## 5. Связи с другими концепциями

- [[Dockerfile и слои образа]] — Docker build — типичный шаг CI пайплайна
- [[Kubernetes pod deployment service]] — kubectl deploy — типичный шаг CD пайплайна
- [[Git merge vs rebase]] — CI запускается на каждый PR/merge request

## 6. Ответ на собесе (2 минуты)

CI/CD — автоматизация пути кода от коммита до production. **CI** (Continuous Integration) — при каждом push автоматически: compile, unit tests, static analysis, сборка образа. Быстрая обратная связь, что код рабочий.

**CD** (Continuous Delivery/Deployment) — доставка артефакта в среды. Delivery: деплой в prod по нажатию кнопки. Deployment: полностью автоматически.

**GitLab CI** — конфигурация в `.gitlab-ci.yml` рядом с кодом: stages, jobs, artifacts, environments. Удобно для проектов на GitLab. **Jenkins** — отдельный сервер, Jenkinsfile, тысячи плагинов, высокая гибкость — подходит для сложных legacy-пайплайнов.

Важные практики: секреты — только в переменных среды (не в коде), кэш maven-зависимостей между запусками, деплой в prod — всегда с ручным подтверждением.

## Шпаргалка

| Этап | Что происходит |
|------|----------------|
| CI: Build | `mvn compile` |
| CI: Test | `mvn test` + junit report |
| CI: Analyze | SonarQube, coverage |
| CI: Package | `docker build && docker push` |
| CD: Staging | `kubectl set image` (авто) |
| CD: Prod | `kubectl set image` (ручное OK) |

| | GitLab CI | Jenkins |
|--|-----------|---------|
| **Config** | `.gitlab-ci.yml` | `Jenkinsfile` |
| **Агенты** | GitLab Runners | Jenkins Agents |
| **Когда** | Новые проекты | Legacy/сложные |

**Связи:**
- [[Dockerfile и слои образа]]
- [[Kubernetes pod deployment service]]
- [[Git merge vs rebase]]

**Hexlet:**
- [[Непрерывная интеграция (CI)]]

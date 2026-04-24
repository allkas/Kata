---
tags: [java, web, http, hexlet]
source: "Java Веб-технологии"
---

# Микрофреймворк Javalin

  * Установка
  * Запуск
  * Внесение изменений



Цикл «запрос-обработка-ответ» включает множество элементов, которые идентичны для всех сайтов. Поэтому возникли так называемые **фреймворки** — библиотеки, которые определяют структуру программы. В этом их отличие от обычных библиотек. Благодаря фреймворкам можно сосредоточиться на логике сайта, а не на продумывании базовой архитектуры или разработке вспомогательных инструментов.

Веб-фреймворки подразделяются на две большие группы:

  * Фреймворки
  * Микрофреймворки



Микрофреймворки устроены значительно проще. Они содержат только минимально необходимую обвязку для комфортной работы в архитектуре HTTP — это «запрос-ответ». Они идеально подходят для обучения, потому что просты и не отвлекают от главного.

В Java таким микрофреймворком стал Javalin. В этом уроке мы начнем изучать принципы работы веб-приложений через призму этого микрофреймворка. Изученные здесь концепции одинаково работают во всех остальных фреймворках, включая Spring Boot, который изучается в следующих курсах.

## Установка

Для начала создайте Gradle-проект со следующими параметрами:

  * Название — _HexletJavalin_
  * Группа — _org.example_
  * Версия — _1.0-SNAPSHOT_



Это можно сделать через редактор или с помощью команды `gradle init`, как показано ниже: 
    
    
    mkdir HexletJavalin
    cd HexletJavalin
    gradle init
    
    Select type of project to generate:
      1: basic
      2: application
      3: library
      4: Gradle plugin
    Enter selection (default: basic) [1..4]
    
    Select build script DSL:
      1: Kotlin
      2: Groovy
    Enter selection (default: Kotlin) [1..2]
    
    Project name (default: HexletJavalin):
    Generate build using new APIs and behavior (some features may change in the next minor release)? (default: no) [yes, no]
    
    > Task :init
    To learn more about Gradle by exploring our Samples at https://docs.gradle.org/8.2.1/samples
    
    BUILD SUCCESSFUL in 10s
    2 actionable tasks: 2 executed
    
    tree -a
    .
    ├── .gitattributes
    ├── .gitignore
    ├── build.gradle.kts
    ├── gradle
    │   └── wrapper
    │       ├── gradle-wrapper.jar
    │       └── gradle-wrapper.properties
    ├── gradlew
    ├── gradlew.bat
    └── settings.gradle.kts
    

Проверьте, выглядит ли ваш файл _build.gradle.kts_ так же, как в примере ниже: 
    
    
    import org.gradle.api.tasks.testing.logging.TestExceptionFormat
    import org.gradle.api.tasks.testing.logging.TestLogEvent
    
    plugins {
        id("java")
        application
    }
    
    application {
        mainClass.set("org.example.hexlet.HelloWorld")
    }
    
    group = "org.example"
    version = "1.0-SNAPSHOT"
    
    repositories {
        mavenCentral()
    }
    
    dependencies {
        // Версии зависимостей могут отличаться
        // Здесь мы сразу подключаем зависимости,
        // которые понадобятся во время обучения
        implementation("io.javalin:javalin:6.1.3")
        implementation("org.slf4j:slf4j-simple:2.0.7")
        implementation("io.javalin:javalin-rendering:6.1.3")
        implementation("gg.jte:jte:3.1.9")
        testImplementation(platform("org.junit:junit-bom:5.9.1"))
        testImplementation("org.junit.jupiter:junit-jupiter")
    }
    
    tasks.test {
        useJUnitPlatform()
        // https://technology.lastminute.com/junit5-kotlin-and-gradle-dsl/
        testLogging {
            exceptionFormat = TestExceptionFormat.FULL
            events = mutableSetOf(TestLogEvent.FAILED, TestLogEvent.PASSED, TestLogEvent.SKIPPED)
            // showStackTraces = true
            // showCauses = true
            showStandardStreams = true
        }
    }
    

Добавьте директорию для хранения исходных файлов: 
    
    
    mkdir -p src/main/java/org/example/hexlet
    

Создайте файл _HelloWorld.java_ со следующим содержимым: 
    
    
    package org.example.hexlet;
    
    import io.javalin.Javalin;
    
    public class HelloWorld {
        public static void main(String[] args) {
            // Создаем приложение
            var app = Javalin.create(config -> {
                config.bundledPlugins.enableDevLogging();
            });
            // Описываем, что загрузится по адресу /
            app.get("/", ctx -> ctx.result("Hello World"));
            app.start(7070); // Стартуем веб-сервер
        }
    }
    

Последний шаг — создайте репозиторий _hexlet-javalin_ на Github и залейте туда код нашего проекта. Он понадобится для экспериментов во время всего курса.

## Запуск

Перейдем к запуску — он выполняется командой `./gradlew run`. Во время выполнения задачи Gradle скачивает зависимости, компилирует проект и запускает веб-сервер, встроенный в Javalin: 
    
    
    ./gradlew run
    
    # Для удобства восприятия мы убрали часть вывода
    > Task :run
    [main] INFO io.javalin.Javalin - JAVALIN HANDLER REGISTRATION DEBUG LOG: GET[/]
           __                  ___          ______
          / /___ __   ______ _/ (_)___     / ____/
     __  / / __ `/ | / / __ `/ / / __ \   /___ \
    / /_/ / /_/ /| |/ / /_/ / / / / / /  ____/ /
    \____/\__,_/ |___/\__,_/_/_/_/ /_/  /_____/
    
           https://javalin.io/documentation
    
    [main] INFO io.javalin.Javalin - Listening on http://localhost:7070/
    [main] INFO io.javalin.Javalin - You are running Javalin 5.6.1 (released June 22, 2023).
    [main] INFO io.javalin.Javalin - Javalin started in 417ms \o/
    ----------------------------------------------------------------------------------
    <=========----> 75% EXECUTING [7m 10s]
    > :run
    

По умолчанию сервер стартует на _http://localhost:7070_. Если открыть адрес в браузере, появится надпись _Hello World_. Одновременно с этим, веб-сервер выведет такие строки в том месте, где мы его запустили: 
    
    
    [JettyServerThreadPool-27] INFO io.javalin.Javalin - JAVALIN REQUEST DEBUG LOG:
    Request: GET [/]
        Matching endpoint-handlers: [GET=/]
    Response: [200 OK], execution took 13.01 ms
        Headers: {Date=Sun, 16 Jul 2023 00:46:28 GMT, Content-Type=text/plain}
        Body is 11 bytes (starts on next line):
        Hello World
    

Этот вывод называется **логом**. Он помогает понять, как браузер взаимодействует с веб-сервером. На каждый запрос в логе появляются новые строчки, которые показывают:

  * Какой запрос пришел на сервер
  * Что сервер сделал в ответ на запрос
  * Чтобы было в полученном запросе (метод, адрес, параметры, заголовки, тело)
  * Есть ли в коде ошибки, из-за которых возникают исключения



В будущем мы не раз будем обращаться к логу для отладки.

Теперь вы умеете запускать веб-сервер Javalin. Чтобы остановить его, можно воспользоваться командой `Ctrl-C`.

## Внесение изменений

Когда веб-сервер запускается, исходный код компилируется и загружается в память. Любые дальнейшие изменения в коде никак не повлияют на запущенное приложение. Это создает неудобства во время разработки — приходится перезапускать сервер каждый раз, когда мы хотим проверить результат изменений. Но для наших задач это не проблема.

* * *

#### Самостоятельная работа

  1. Выполните все шаги из этого урока на своем компьютере
  2. Создайте на GitHub репозиторий с именем _hexlet-javalin_ и залейте в него код нашего проекта. Этот проект понадобится нам в дальнейших уроках



* * *

#### Дополнительные материалы

  1. Описание установки в официальной документации
  2. Репозиторий с примерами из курса

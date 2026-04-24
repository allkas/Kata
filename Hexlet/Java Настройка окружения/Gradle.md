---
tags: [java, setup, hexlet]
source: "Java Настройка окружения"
---

# Gradle

Поговорим о принципах работы Gradle. Базовая единица работы Gradle — это задача. Каждый раз когда мы хотим запустить Gradle, мы должны точно знать, какую задачу хотим запустить. Вот лишь некоторые из них: 
    
    
    # Вывод списка задач это тоже задача
    # Список выводится в сокращенном виде
    ./gradlew tasks
    
    > Task :tasks
    
    ------------------------------------------------------------
    Tasks runnable from root project 'hexlet-gradle-project'
    ------------------------------------------------------------
    
    Application tasks
    -----------------
    run - Runs this project as a JVM application
    
    Build tasks
    -----------
    build - Assembles and tests this project.
    clean - Deletes the build directory.
    jar - Assembles a jar archive containing the main classes.
    
    Build Setup tasks
    -----------------
    init - Initializes a new Gradle build.
    
    Documentation tasks
    -------------------
    javadoc - Generates Javadoc API documentation for the main source code.
    
    Verification tasks
    ------------------
    check - Runs all checks.
    test - Runs the test suite.
    

Например, если мы хотим выполнить сборку проекта, то надо запустить `./gradlew build`, а если получить готовый jar-файл, то `./gradlew jar`. Для запуска приложения, как программы достаточно набрать `./gradlew run`.

Многие задачи имеют общие части. Сборка проекта и формирование jar-файла требуют компиляции. Gradle решает это через зависимости задач друг от друга. Когда мы запускаем `./gradlew build`, то внутри запускаются другие задачи, которые выполняют разные манипуляции с кодом. Gradle умеет показывать эти зависимости: 
    
    
    # Флаг --dry-run показывает то, как будет выполняться задача
    # Что она в себя включает
    
    ./gradlew jar --dry-run # jar
    
    :app:compileJava SKIPPED
    :app:processResources SKIPPED
    :app:classes SKIPPED
    :app:jar SKIPPED
    
    BUILD SUCCESSFUL in 556ms
    
    ./gradlew build --dry-run # build
    
    :app:compileJava SKIPPED
    :app:processResources SKIPPED
    :app:classes SKIPPED
    :app:jar SKIPPED
    :app:startScripts SKIPPED
    :app:distTar SKIPPED
    :app:distZip SKIPPED
    :app:assemble SKIPPED
    :app:compileTestJava SKIPPED
    :app:processTestResources SKIPPED
    :app:testClasses SKIPPED
    :app:test SKIPPED
    :app:check SKIPPED
    :app:build SKIPPED
    
    BUILD SUCCESSFUL in 610ms
    

По выводу выше мы видим, что сборка jar-файла это один из этапов выполнения задачи _build_. А компиляция, как ни странно, это лишь малая часть процесса, выполняемая в самом начале: 
    
    
    ./gradlew compileJava
    
    BUILD SUCCESSFUL in 682ms
    1 actionable task: 1 executed
    

## Разработка с Gradle

Основной редактор у всех Java разработчиков это Idea. Но Idea не просто редактор, такие программы называют IDE (интегрированная среда разработки). Она глубоко интегрирована с инструментами Java и позволяет запускать код прямо изнутри. Idea интегрирована с Gradle, знает как вызывать его задачи и делает это либо сама, либо по кнопке. Фактически пользоваться Gradle через консоль нужно только в случае отладки, когда мы пытаемся разобраться в ошибках.

Теперь пришла пора попробовать завести проект на Gradle в Idea. Лучше всего это сделать по официальной документации с картинками: https://www.jetbrains.com/help/idea/gradle.html

* * *

#### Самостоятельная работа

  1. Склонируйте себе эталонный репозиторий. Перейдите в него и выполните все шаги из урока
  2. Запустите приложение при помощи команды `./gradlew run` и изучите получившийся вывод



* * *

#### Дополнительные материалы

  1. Настроенный Gradle-проект

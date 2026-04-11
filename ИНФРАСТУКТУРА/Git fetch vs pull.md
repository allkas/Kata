---
title: Git fetch vs pull
tags: [git, fetch, pull, vcs]
parent: [[00 Индекс всех тем]]
prev: [[Git merge vs rebase]]
next: [[Git cherry-pick]]
---
# 📥 Git fetch vs pull
## 🧠 Ментальная модель
| Команда | Что делает | Аналогия |
|---------|-----------|----------|
| `git fetch` | Скачивает изменения **без слияния** | Посмотреть, что в ящике, не забирая |
| `git pull` | Скачивает + сразу сливает (merge/rebase) | Забрать всё из ящика сразу |
## 📊 Сравнение
| Характеристика | `fetch` | `pull` |
|----------------|---------|--------|
| Загружает изменения | ✅ | ✅ |
| Обновляет рабочую копию | ❌ | ✅ |
| Создаёт merge commit | ❌ | Может |
| Безопасность | Высокая | Средняя |
## ⚡ Рекомендация
```bash
# ❌ Не делайте так
git pull origin main   # непонятно, что произойдёт
# ✅ Делайте так
git fetch origin main
git diff origin/main   # посмотреть изменения
git merge origin/main  # или rebase
```
## 🎯 Настройка поведения pull

```bash

# merge (по умолчанию)
git pull --no-rebase
# rebase
git pull --rebase
```
## 🔗 Связано

- [[Git merge vs rebase]]
    
- [[Git cherry-pick]]
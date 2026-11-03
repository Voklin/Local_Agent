# Приёмка свежего пакета LESHY — 3 ноября 2026

## Артефакт и границы проверки

Создан новый `artifacts/windows-20261103/LESHY-7.0.1-setup-x64.exe`, 427930689 байт, и новый `win-unpacked/LESHY.exe`. Старый output `artifacts/windows` не использовался для этой приёмки. Installer не устанавливался в пользовательский профиль и не публиковался.

Сборка выполнена из текущего development checkout на HEAD `9572082` с сохранёнными незакоммиченными изменениями. Это не воспроизведение чистого commit. Состав runtime-исходников, версии и SHA256 артефактов сохраняются в `artifacts/development-2026-11-03/build-manifest.json`.

Python 3.12.14; все установленные пакеты из закреплённого `requirements-build.txt` совпали с указанными версиями. Закреплённый Code-OSS/VSCodium подготовлен из проверенного локального ZIP; runtime и LESHY-ресурсы включены в пакет. Frozen Core пересобран перед упаковкой. Подпись executable отключена существующей конфигурацией сборки.

## Текущие результаты

| Проверка | Результат | Свидетельство |
|---|---|---|
| Новый frozen Core | PASS | `freeze.log` |
| Подпроцессы frozen Core | 17 тестов, OK, 35.032 s | `frozen-bridge.log` |
| NSIS | PASS, exit 0 | `package.log` |
| Путь package smoke | 4 проверки PASS: LESHY, только Neutral, оба, explicit output | `tests/electron/packaged-path.test.mjs` |
| Чистый временный профиль и stripped PATH | PASS | `packaged-native-smoke-final.log` |
| Миграция legacy Chat/Voice в SQLite | PASS, исходные JSON сохранены | тот же smoke |
| Закрытие и повторный запуск | PASS, настройки сохранены | два package-exit с code 0 |
| Отсутствие API-ключей в preferences/log | PASS на fixture-ключах | тот же smoke |
| Вложенная packaged IDE | PASS | `packaged-ide-result.json` |
| Frozen Core → webview → diff approval | PASS; до approval файл не менялся | тот же IDE result |
| Editor-owned запись → Undo → Save | PASS, исходный файл восстановлен | тот же IDE result |

Логи и скопированные JSON находятся в `artifacts/development-2026-11-03/`. HTTP-ответы синтетические, реальная LLM не загружалась. Успех этих тестов не является оценкой качества модели.

При разработке расширенного fixture первая проверка перезапуска обнаружила сброс temperature самим тестом: helper передавал только memory_updates. Helper исправлен с сохранением текущих settings; полный повторный сценарий прошёл. Это не исправление производственного Core.

## Незакрытые release gates

- **UNVERIFIED:** установка нового NSIS на чистой Windows без инструментов разработчика.
- **UNVERIFIED:** обновление установленного Neutral с копией старого профиля, удаление и сохранение пользовательских данных. Тест legacy JSON в unpacked приложении покрывает только часть этого пути.
- **UNVERIFIED:** выполнение обновлённого Windows GitHub Actions job на commit, содержащем все изменения. Локальный GUI PASS не заменяет remote CI.
- **UNVERIFIED:** длительные реальные модельные задачи, аппаратные пределы и полная accessibility-приёмка.

До выполнения первых двух пунктов installer следует считать кандидатом для приёмки, а не завершённым релизом. Перед публичным выпуском требуется отдельное разрешение на публикацию и актуальная проверка выбранной ревизии.

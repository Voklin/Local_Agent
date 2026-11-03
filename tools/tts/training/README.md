# Локальная пробная Serena для Piper

Полный план, проверенные версии и границы: [SERENA_TRAINING_PLAN](../../../docs/SERENA_TRAINING_PLAN.md).
Запускать из корня LocalAgent. Среда генерации — существующий `tts-runtime`;
среда обучения — `build/voice-training/venv`. Датасет и модели хранятся в artifacts.

Корпус `serena_texts.txt`, WAV, checkpoints и обученные веса остаются локальными
и не публикуются в GitHub. Для новой среды подготовьте собственный UTF-8 файл
`serena_texts.txt` рядом с generate_serena.py: по одной фразе на строке. Исходные
скрипты обучения доступны отдельно от данных.

```powershell
# Подготовка/продолжение датасета (готовые ID не генерируются повторно):
& "$env:LOCALAPPDATA/LocalCodingAgent/tts-runtime/Scripts/python.exe" tools/tts/training/generate_serena.py --output artifacts/voice-training/serena-v1 --limit 320 --batch-size 2

# Один настоящий шаг для проверки окружения:
& ./build/voice-training/venv/Scripts/python.exe tools/tts/training/run_training.py --dataset artifacts/voice-training/serena-v1 --smoke

# Конвейер после завершения генерации:
& ./build/voice-training/venv/Scripts/python.exe tools/tts/training/pipeline.py --dataset artifacts/voice-training/serena-v1
```

При работающем generator конвейеру можно передать `--generator-pid <PID>`:
он дождётся выхода процесса. Не запускайте эти команды повторно, пока worker жив.
На Windows конвейер удерживает файл pipeline.lock; состояние сохраняет атомарно.
При ошибках проверяйте logs. Генерация требует STT на localhost:8080/inference.
Автоматический pipeline без `--generator-pid` требует уже завершённый корпус.

`serena_texts.txt` содержит исходные тексты; `texts()` добавляет бытовые фразы.
`normalize()` нужен только ASR проверке, исходные тексты обучения не заменяются STT.
`run_training.py` конвертирует метаданные базового checkpoint, выполняет warmstart
и задаёт Windows eSpeak data dir. `export_and_evaluate.py` экспортирует выбранный
обученный checkpoint в ONNX и проверяет CPU синтез отдельно от обучения.
`pipeline.py` запускает зависимые этапы последовательно, записывает точные ошибки
и не объявляет модель готовой до итоговой проверки. Важна последующая оценка на слух.

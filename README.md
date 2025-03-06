# Бложик

## Установка

- клонировать репозиторий
- установить зависимости
```shell
cd qa_stand_api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```
- запустить сервер
```
fastapi dev main.py
```

## Баги
[Список известных багов](./docs/issues.md)
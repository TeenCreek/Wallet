# Wallet Service

## Описание

Wallet Service - это приложение на Django, которое позволяет управлять кошельками и операциями с ними. Проект использует PostgreSQL в качестве базы данных и запускается в Docker-контейнерах.

## Стек технологий

- Python
- Django
- PostgreSQL
- Docker
- Docker Compose
- pytest для тестирования

## Установка и запуск проекта

### 1. Клонирование репозитория

Клонируйте проект из Docker Hub:

```
docker pull rakk69/wallet
```

Или из GitHub

```
git clone git@github.com:TeenCreek/Wallet.git
```

### 2. Создание .env файла

Создайте файл .env в корне проекта и добавьте следующие переменные окружения:

```
DB_HOST=db
DB_PORT=5432
DB_NAME=wallet
DB_USER=postgres
DB_PASS=your_postgres_password
SECRET_KEY=your_secret_key
```

### 3. Запуск проекта

Перейдите в директорию с проектом и выполните команду:

```
docker-compose up --build
```

Если образы уже собраны, просто выполните:

```
docker-compose up
```

### 4. Создание суперпользователя

Для создания суперпользователя выполните команду:

```
docker-compose exec web python manage.py createsuperuser
```

Или войдите по уже готовому аккаунту:

```
логин: admin
пароль: admin
```

### 5. Удаление контейнеров

Если вам нужно удалить все контейнеры и образы, выполните:

```
docker-compose down --volumes
```

# Примеры использования API

## Сделать транзакцию

```
POST api/v1/wallets/<WALLET_UUID>/operation

{
    operationType: DEPOSIT or WITHDRAW,
    amount: 1000
}
```

## Получить баланс кошелька

```
GET api/v1/wallets/{WALLET_UUID}
```

## Создать кошелек

```
POST api/v1/wallets/

{
    "balance": "100"
}
```

## Документация API

```
/api/swagger/
```

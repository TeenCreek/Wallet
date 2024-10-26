from rest_framework import serializers


def validate_balance(value):
    """Валидация баланса: он не может быть отрицательным."""

    if value < 0:
        raise serializers.ValidationError('Баланс не может быть отрицательным')

    return value


def validate_amount(value):
    """Валидация транзакции: сумма должна быть больше 0."""

    if value <= 0:
        raise serializers.ValidationError(
            'Сумма должна быть положительным числом и больше 0'
        )

    return value

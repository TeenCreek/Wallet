from rest_framework import serializers

from .models import Transaction, Wallet
from .validators import validate_amount, validate_balance


class WalletSerializer(serializers.ModelSerializer):
    """Сериализатор для кошелька."""

    class Meta:
        model = Wallet
        fields = ('id', 'balance', 'created_at')


class WalletCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания кошелька."""

    class Meta:
        model = Wallet
        fields = ('balance',)

    def validate_balance(self, value):
        """Валидация поля balance."""

        return validate_balance(value)


class TransactionSerializer(serializers.Serializer):
    """Сериализатор для транзакций."""

    operation_type = serializers.ChoiceField(
        choices=Transaction.Operation.choices,
        help_text='Тип операции: DEPOSIT или WITHDRAW',
    )

    amount = serializers.DecimalField(
        max_digits=20,
        decimal_places=2,
        help_text='Сумма для пополнения или снятия',
    )

    def validate_amount(self, value):
        return validate_amount(value)

from uuid import uuid4

from django.db import models


class Wallet(models.Model):
    """Модель для кошелька."""

    id = models.UUIDField(
        'ID кошелька',
        primary_key=True,
        default=uuid4,
        editable=False,
    )
    balance = models.DecimalField(
        'Баланс кошелька',
        max_digits=30,
        decimal_places=2,
        default=0,
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Кошелек'
        verbose_name_plural = 'Кошельки'

    def __str__(self):
        return f'Кошелек {self.id} имеет баланс {self.balance}'


class Transaction(models.Model):
    """Модель для типа транзакции."""

    class Operation(models.TextChoices):
        """Типы операций для транзакции."""

        DEPOSIT = 'DEPOSIT', 'Пополнение'
        WITHDRAW = 'WITHDRAW', 'Снятие'

    wallet = models.ForeignKey(
        Wallet,
        related_name='transactions',
        verbose_name='Кошелек',
        on_delete=models.CASCADE,
    )
    operation = models.CharField(
        'Тип операции',
        max_length=10,
        choices=Operation.choices,
    )
    amount = models.DecimalField('Сумма', max_digits=20, decimal_places=2)
    created_at = models.DateTimeField(
        'Дата проведения транзакции', auto_now_add=True
    )

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'

    def __str__(self):
        return f'{self.operation} {self.amount} для кошелька {self.wallet.id}'

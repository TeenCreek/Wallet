from django.contrib import admin

from .forms import WalletForm
from .models import Transaction, Wallet

EMPTY_VALUE = '-ПУСТО-'


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    """Админка для кошельков."""

    form = WalletForm
    list_display = ('id', 'balance', 'created_at')
    search_fields = ('id',)
    ordering = ('id',)
    empty_value_display = EMPTY_VALUE

    def has_change_permission(self, request, obj=None):
        """Запретить изменение кошелька."""

        return False


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """Админка для транзакций."""

    list_display = ('wallet', 'operation', 'amount', 'created_at')
    list_filter = ('wallet', 'created_at')
    search_fields = ('wallet', 'operation')
    readonly_fields = ('wallet', 'operation', 'amount', 'created_at')
    empty_value_display = EMPTY_VALUE

    def has_change_permission(self, request, obj=None):
        """Запретить изменение транзакций."""

        return False

    def has_add_permission(self, request):
        """Запретить создание транзакций."""
        return False

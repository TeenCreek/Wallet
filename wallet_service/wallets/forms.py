from django import forms

from .models import Wallet


class WalletForm(forms.ModelForm):
    """Форма для редактирования кошелька."""

    class Meta:
        model = Wallet
        fields = ('balance',)

    def clean_balance(self):
        """Валидация поля баланса."""

        balance = self.cleaned_data['balance']

        if balance < 0:
            raise forms.ValidationError('Баланс не может быть отрицательным')
        return balance

# Generated by Django 5.1.2 on 2024-10-26 10:15

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID кошелька')),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=30, verbose_name='Баланс кошелька')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'Кошелек',
                'verbose_name_plural': 'Кошельки',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('operation', models.CharField(choices=[('DEPOSIT', 'Пополнение'), ('WITHDRAW', 'Снятие')], max_length=10, verbose_name='Тип операции')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Сумма')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата проведения транзакции')),
                ('wallet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='wallets.wallet', verbose_name='Кошелек')),
            ],
            options={
                'verbose_name': 'Транзакция',
                'verbose_name_plural': 'Транзакции',
                'ordering': ('-created_at',),
            },
        ),
    ]

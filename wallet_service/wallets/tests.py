import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from wallets.models import Wallet

INITIAL_BALANCE = 1000
DEPOSIT_AMOUNT = '200.00'
WITHDRAW_AMOUNT = '300.00'
INSUFFICIENT_WITHDRAW_AMOUNT = '1500.00'
CREATED_BALANCE = '500.00'
RETRIEVED_BALANCE = '1000.00'


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def wallet():
    """Создание кошелька с начальным балансом."""

    return Wallet.objects.create(balance=INITIAL_BALANCE)


@pytest.mark.django_db
def test_create_wallet(api_client):
    """Тест на создание нового кошелька."""

    url = reverse('wallets:wallets-list')
    data = {'balance': 500}
    response = api_client.post(url, data, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['balance'] == CREATED_BALANCE
    assert Wallet.objects.filter(balance=500).exists()


@pytest.mark.django_db
def test_retrieve_wallet(api_client, wallet):
    """Тест на получение информации о кошельке."""

    url = reverse('wallets:wallets-detail', kwargs={'pk': wallet.id})
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['balance'] == RETRIEVED_BALANCE


@pytest.mark.django_db
def test_deposit_wallet(api_client, wallet):
    """Тест на пополнение кошелька."""

    url = reverse(
        'wallets:wallets-perform-operation', kwargs={'pk': wallet.id}
    )
    data = {'operation_type': 'DEPOSIT', 'amount': DEPOSIT_AMOUNT}
    response = api_client.post(url, data, format='json')

    assert response.status_code == status.HTTP_200_OK
    wallet.refresh_from_db()
    assert wallet.balance == INITIAL_BALANCE + 200


@pytest.mark.django_db
def test_withdraw_wallet(api_client, wallet):
    """Тест на снятие средств с кошелька."""

    url = reverse(
        'wallets:wallets-perform-operation', kwargs={'pk': wallet.id}
    )
    data = {'operation_type': 'WITHDRAW', 'amount': WITHDRAW_AMOUNT}
    response = api_client.post(url, data, format='json')

    assert response.status_code == status.HTTP_200_OK
    wallet.refresh_from_db()
    assert wallet.balance == INITIAL_BALANCE - 300


@pytest.mark.django_db
def test_withdraw_insufficient_funds(api_client, wallet):
    """Тест на ошибку при недостатке средств для снятия."""

    url = reverse(
        'wallets:wallets-perform-operation', kwargs={'pk': wallet.id}
    )
    data = {
        'operation_type': 'WITHDRAW',
        'amount': INSUFFICIENT_WITHDRAW_AMOUNT,
    }
    response = api_client.post(url, data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['error'] == 'Недостаточно средств'

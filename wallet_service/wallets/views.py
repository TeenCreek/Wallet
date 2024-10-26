from django.db import transaction
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.response import Response

from .models import Transaction, Wallet
from .serializers import (
    TransactionSerializer,
    WalletCreateSerializer,
    WalletSerializer,
)


class WalletViewSet(viewsets.ViewSet):
    """Вьюсет для кошелька."""

    @swagger_auto_schema(
        operation_description='Создание нового кошелька',
        request_body=WalletCreateSerializer,
        responses={
            201: WalletSerializer(),
            400: openapi.Response(description='Неверный запрос'),
        },
    )
    def create(self, request):
        """Создание нового кошелька."""
        serializer = WalletCreateSerializer(data=request.data)

        if serializer.is_valid():
            wallet = serializer.save()
            response_serializer = WalletSerializer(wallet)

            return Response(
                response_serializer.data, status=status.HTTP_201_CREATED
            )

        return Response(
            {'error': 'Неверный запрос', 'details': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @swagger_auto_schema(
        operation_description='Получение баланса кошелька по его ID',
        responses={
            200: WalletSerializer(),
            404: openapi.Response(description='Кошелек не найден'),
        },
    )
    def retrieve(self, request, pk=None):
        """Получение баланса кошелька по его ID."""

        try:
            wallet = Wallet.objects.get(pk=pk)
            serializer = WalletSerializer(wallet)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Wallet.DoesNotExist:
            raise NotFound({'error': 'Кошелек не найден'})

    @swagger_auto_schema(
        operation_description='Выполнение операции DEPOSIT или WITHDRAW на указанном кошельке',
        request_body=TransactionSerializer,
        responses={
            200: openapi.Response(
                description='Баланс кошелька',
                examples={'application/json': {'balance': 2000}},
            ),
            400: openapi.Response(
                description='Недостаточно средств или неверный запрос'
            ),
            404: openapi.Response(description='Кошелек не найден'),
        },
    )
    @action(detail=True, methods=['post'], url_path='operation')
    def perform_operation(self, request, pk=None):
        """Выполнение операции DEPOSIT или WITHDRAW на указанном кошельке."""

        serializer = TransactionSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {'error': 'Неверный запрос', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            with transaction.atomic():
                wallet = Wallet.objects.select_for_update().get(pk=pk)

                operation_type = serializer.validated_data['operation_type']
                amount = serializer.validated_data['amount']

                if operation_type == Transaction.Operation.WITHDRAW:
                    if wallet.balance < amount:
                        return Response(
                            {'error': 'Недостаточно средств'},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                    wallet.balance -= amount

                elif operation_type == Transaction.Operation.DEPOSIT:
                    wallet.balance += amount

                wallet.save()

                Transaction.objects.create(
                    wallet=wallet, operation=operation_type, amount=amount
                )

            return Response(
                {'balance': wallet.balance}, status=status.HTTP_200_OK
            )

        except Wallet.DoesNotExist:
            raise NotFound({'error': 'Кошелек не найден'})
        except ValidationError as e:
            return Response(
                {'error': 'Ошибка валидации', 'details': str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {'error': 'Внутренняя ошибка сервера', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

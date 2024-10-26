from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.routers import DefaultRouter

from .views import WalletViewSet

app_name = 'wallets'

schema_view = get_schema_view(
    openapi.Info(
        title='Wallet API',
        default_version='v1',
        description='API для работы с кошельками',
    ),
    public=True,
)


v1_router = DefaultRouter()

v1_router.register('wallets', WalletViewSet, basename='wallets')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path(
        'swagger/',
        schema_view.with_ui(
            'swagger',
            cache_timeout=0,
        ),
        name='swagger',
    ),
    path(
        'redoc/',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='redoc',
    ),
]

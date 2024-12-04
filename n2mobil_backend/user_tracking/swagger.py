from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
    openapi.Info(
        title="N2Mobil API",
        default_version='v1',
        description="API documentation for N2Mobil with x-api-key authentication",
        contact=openapi.Contact(email="info@n2mobil.com.tr"),
    ),
    public=True,
    permission_classes=(AllowAny,),  # Swagger erişimine herkes izinli
)
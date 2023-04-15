from django.contrib import admin as django_admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import re_path

# openapi documentation
schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('django_admin/', django_admin.site.urls),

    re_path(r'^docs/$', schema_view.with_ui('swagger',
            cache_timeout=0), name='schema-swagger-ui'),
    re_path(
        "api/v1/auth/", include(("api.v1.auth.urls", "auth"),
                                namespace="api_v1_auth")
    ),
    re_path(
        "api/v1/user/", include(("api.v1.user.urls", "user"),
                                namespace="api_v1_user")
    ),
    re_path(
        "api/v1/admin/", include(("api.v1.admin.urls", "admin"),
                                namespace="api_v1_admin")
    ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

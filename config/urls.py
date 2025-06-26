from django.contrib import admin
from django.conf import settings
from django.urls import re_path, include
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from django.conf import settings
from fundinfo.users import views

urlpatterns = [
    path("schema/", SpectacularAPIView.as_view(api_version="v1"), name="schema"),
    path("", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path('admin/', admin.site.urls),
    path('api/', include(('fundinfo.api.urls', 'api'))),
    re_path(r'^core/', include(('fundinfo.core.urls', 'core'))),
    re_path(r'^core/auth/', include(('django.contrib.auth.urls', 'auth'))),
    re_path(r'^core/auth/signup/', views.SignUpView.as_view(), name='signup'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

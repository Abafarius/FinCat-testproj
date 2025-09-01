# back/core/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from orgs.views import LicenseViewSet  # + FinancialOrgViewSet, если там же

router = DefaultRouter()

router.register(r'licenses', LicenseViewSet, basename='license')  # ⬅️ ДОБАВЬ ЭТО

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/auth/", include("users.urls")),
    path("api/auth/token/", __import__("rest_framework_simplejwt.views").simplejwt.views.TokenObtainPairView.as_view()),
    path("api/auth/refresh/", __import__("rest_framework_simplejwt.views").simplejwt.views.TokenRefreshView.as_view()),
]


from django.conf import settings
from django.conf.urls.static import static
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

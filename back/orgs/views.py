from rest_framework.viewsets import ModelViewSet
from rest_framework import viewsets, permissions, filters
from .models import FinancialOrg, License
from .serializers import FinancialOrgSerializer, LicenseSerializer
from .permissions import IsAdminOrReadOnly

class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated  # у нас чтение тоже с токеном
        return bool(request.user and request.user.is_staff)

class FinancialOrgViewSet(ModelViewSet):
    queryset = FinancialOrg.objects.all().order_by("name")
    serializer_class = FinancialOrgSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ["bin","name"]

class LicenseViewSet(viewsets.ModelViewSet):
    queryset = License.objects.all().order_by("id")
    serializer_class = LicenseSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["code"]
    ordering_fields = ["code", "issued_at", "id"]

from rest_framework.viewsets import ModelViewSet
from .models import FinancialOrg, License
from .serializers import FinancialOrgSerializer, LicenseSerializer
from .permissions import IsAdminOrReadOnly

class FinancialOrgViewSet(ModelViewSet):
    queryset = FinancialOrg.objects.all().order_by("name")
    serializer_class = FinancialOrgSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ["bin","name"]

class LicenseViewSet(ModelViewSet):
    queryset = License.objects.all().order_by("code")
    serializer_class = LicenseSerializer
    permission_classes = [IsAdminOrReadOnly]

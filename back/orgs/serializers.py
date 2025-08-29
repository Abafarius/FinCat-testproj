from rest_framework import serializers
from .models import FinancialOrg, License

class LicenseSerializer(serializers.ModelSerializer):
    class Meta: model = License; fields = "__all__"

class FinancialOrgSerializer(serializers.ModelSerializer):
    licenses = LicenseSerializer(many=True, read_only=True)
    license_ids = serializers.PrimaryKeyRelatedField(
        many=True, write_only=True, queryset=License.objects.all(), source="licenses"
    )
    class Meta:
        model = FinancialOrg
        fields = ("id","name","bin","logo","licenses","license_ids")

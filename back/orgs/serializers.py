from rest_framework import serializers
from .models import FinancialOrg, License

class LicenseSerializer(serializers.ModelSerializer):
    code = serializers.CharField(max_length=255)

    class Meta:
        model = License
        fields = ("id", "code", "issued_at")

    def validate_code(self, value):
        v = value.strip()
        if not v:
            raise serializers.ValidationError("Код лицензии не может быть пустым")
        return v

class FinancialOrgSerializer(serializers.ModelSerializer):
    licenses = LicenseSerializer(many=True, read_only=True)
    license_ids = serializers.PrimaryKeyRelatedField(
        many=True, write_only=True, queryset=License.objects.all(), source="licenses"
    )
    class Meta:
        model = FinancialOrg
        fields = ("id","name","bin","logo","licenses","license_ids")

from rest_framework import serializers

from core.apps.retail.models import RetailPoint, Employee


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('id', 'last_name', 'first_name', 'middle_name', 'phone', 'email', 'api_key')
        read_only_fields = ('api_key',)


class RetailPointSerializer(serializers.ModelSerializer):
    employees = EmployeeSerializer(many=True, read_only=True)

    class Meta:
        model = RetailPoint
        fields = (
            'id', 'name', 'point_type', 'country', 'city', 'street',
            'house_number', 'daily_revenue', 'employees',
            'created_at', 'updated_at',
        )
        read_only_fields = ('daily_revenue', 'created_at', 'updated_at')

    def validate_name(self, value: str) -> str:
        if len(value) > 50:
            raise serializers.ValidationError('Название не более 50 символов')
        return value

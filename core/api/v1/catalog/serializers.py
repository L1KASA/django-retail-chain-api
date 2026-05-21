from rest_framework import serializers

from core.apps.catalog.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'brand', 'model', 'price', 'release_date', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')

    def validate_brand(self, value):
        if len(value) > 50:
            raise serializers.ValidationError('Бренд длиной не более 50 символов')
        return value

    def validate_model(self, value):
        if len(value) > 25:
            raise serializers.ValidationError('Модель длиной не более 25 символов')
        return value

    def validate_release_date(self, value):
        from datetime import date
        if value > date.today():
            raise serializers.ValidationError('Дата релиза не может быть в будущем времени')
        return value

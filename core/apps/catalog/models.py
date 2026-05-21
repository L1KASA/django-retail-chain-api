from django.core.validators import MinValueValidator
from django.db import models
from core.apps.common.models import TimedBaseModel


class Product(TimedBaseModel):
    brand = models.CharField(
        verbose_name='Бренд',
        max_length=50,
    )
    model = models.CharField(
        verbose_name='Модель',
        max_length=25,
    )
    price = models.DecimalField(
        verbose_name='Цена',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    release_date = models.DateField(
        verbose_name='Дата выхода на рынок',
    )

    class Meta:  # type: ignore[attr-defined]
        verbose_name = 'Продукт'
        verbose_name_plural = 'Каталог продуктов'
        ordering = ['brand', 'model']
        constraints = [
            models.UniqueConstraint(
                fields=['brand', 'model'],
                name='unique_product',
            )
        ]

    def __str__(self):
        return f'{self.brand} {self.model}'
    
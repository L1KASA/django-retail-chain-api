from django.core.validators import MinValueValidator
from django.db import models
from core.apps.common.models import TimedBaseModel


class Inventory(TimedBaseModel):
    product = models.ForeignKey(
        'catalog.Product',
        on_delete=models.CASCADE,
        related_name='inventory_items',
        verbose_name='Продукт',
    )
    retail_point = models.ForeignKey(
        'retail.RetailPoint',
        on_delete=models.CASCADE,
        related_name='inventory_items',
        verbose_name='Торговая точка',
        limit_choices_to={'point_type': 'dealer'},
    )
    quantity = models.PositiveIntegerField(
        verbose_name='Количество',
        default=0,
        validators=[MinValueValidator(0)],
    )

    class Meta:  # type: ignore[attr-defined]
        verbose_name = 'Наличие'
        verbose_name_plural = 'Учет наличия'
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'retail_point'],
                name='unique_product_per_dealer',
            )
        ]

    def __str__(self):
        return f'{self.product} в {self.retail_point.name}: {self.quantity} шт.'

from django.db import models
from django.conf import settings
from core.apps.common.models import TimedBaseModel
from django.db.models import Q
from decimal import Decimal
import uuid


class RetailPoint(TimedBaseModel):
    class PointType(models.TextChoices):
        HEAD_OFFICE = 'head', 'Головной отдел'
        DEALER = 'dealer', 'Дилерский центр'

    name = models.CharField(
        verbose_name='Название',
        max_length=50,
    )
    point_type = models.CharField(
        verbose_name='Тип точки',
        choices=PointType.choices,
        default=PointType.DEALER,
    )
    country = models.CharField(
        verbose_name='Страна',
        max_length=100,
    )
    city = models.CharField(
        verbose_name='Город',
        max_length=100,
    )
    street = models.CharField(
        verbose_name='Улица',
        max_length=200,
    )
    house_number = models.CharField(
        verbose_name='Номер дома',
        max_length=20,
    )
    daily_revenue = models.DecimalField(
        verbose_name='Выручка за день',
        decimal_places=2,
        max_digits=14,
        default=Decimal('0.00'),
    )
    
    class Meta:  # type: ignore[attr-defined]
        verbose_name = 'Торговая точка'
        verbose_name_plural = 'Торговые точки'
        constraints = [
            models.UniqueConstraint(
                fields=['point_type'],
                condition=Q(point_type='head'),
                name='only_one_head_office',
            )
        ]
    
    def __str__(self) -> str:
        return f'{self.name} ({self.get_point_type_display()})'  # type: ignore[attr-defined]
    
    @property
    def is_head_office(self) -> bool:
        return self.point_type == self.PointType.HEAD_OFFICE
    
    @property
    def is_dealer(self) -> bool:
        return self.point_type == self.PointType.DEALER


class Employee(TimedBaseModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='employee',
        verbose_name='Пользователь',
    )
    api_key = models.UUIDField(
        verbose_name='API-ключ',
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )
    retail_point = models.ForeignKey(
        RetailPoint,
        on_delete=models.CASCADE,
        related_name='employees',
        verbose_name='Торговая точка',
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=100,
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=100,
    )
    middle_name = models.CharField(
        verbose_name='Отчество',
        max_length=100,
        blank=True,
    )
    phone = models.CharField(
        verbose_name='Номер телефона',
        max_length=20,
    )

    class Meta:  # type: ignore[attr-defined]
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    @property
    def email(self) -> str:
        return self.user.email
    
    @property
    def full_name(self) -> str:
        return f'{self.last_name} {self.first_name} {self.middle_name}'.strip()
    
    def __str__(self):
        return f'{self.full_name} ({self.retail_point.name})'

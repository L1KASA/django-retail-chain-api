from celery import shared_task

from core.project.containers import get_container
from core.apps.inventory.use_cases.reduce_random_stock import ReduceRandomStockUseCase
from core.apps.retail.models import RetailPoint
from django.core.mail import send_mail


@shared_task
def hourly_stock_reduction_task():
    container = get_container()
    use_case = container.resolve(ReduceRandomStockUseCase)
    return use_case.execute()


@shared_task
def send_low_stock_email_task(dealer_id: int, product_id: int) -> None:
    """Отправка email сотруднику головного отдела"""
    dealer = RetailPoint.objects.get(id=dealer_id)
    product = dealer.inventory_items.get(product_id=product_id).product

    head_office = RetailPoint.objects.get(point_type=RetailPoint.PointType.HEAD_OFFICE)
    head_employee = head_office.employees.first()

    if not head_employee:
        return

    subject = f'Обнулился остаток: {product.brand} {product.model}'
    message = (
        f'Дилерский центр: {dealer.name}\n'
        f'Адрес: {dealer.country}, {dealer.city}, {dealer.street}, {dealer.house_number}\n'
        f'Оборудование: {product.brand} {product.model}\n'
        f'Остаток: 0 шт.'
    )

    send_mail(subject, message, None, [head_employee.email])

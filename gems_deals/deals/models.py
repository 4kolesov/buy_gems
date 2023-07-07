from django.db import models


class Deal(models.Model):
    """Модель сделки."""

    customer = models.CharField(
        verbose_name='Username покупателя',
        max_length=100,
    )
    item = models.CharField(verbose_name='Наименование товара', max_length=100)
    total = models.DecimalField(
        verbose_name='Сумма сделки',
        max_digits=10,
        decimal_places=3,
    )
    quantity = models.IntegerField(verbose_name='Количество товара, шт')
    date = models.DateTimeField(verbose_name='Дата и время регистрации сделки')

    class Meta:
        verbose_name = 'Сделка'
        verbose_name_plural = 'Сделки'
        constraints = [
            models.UniqueConstraint(
                fields=['customer', 'date'],
                name='unique_deal',
            )
        ]
